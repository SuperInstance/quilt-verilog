// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vq_fabric_top.h for the primary calling header

#include "Vq_fabric_top__pch.h"
#include "Vq_fabric_top_q_cell.h"

VL_INLINE_OPT void Vq_fabric_top_q_cell___ico_sequent__TOP__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__connc__DOT__u_cell__0(Vq_fabric_top_q_cell* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    Vq_fabric_top__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vq_fabric_top_q_cell___ico_sequent__TOP__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__connc__DOT__u_cell__0\n"); );
    auto &vlSelfRef = std::ref(*vlSelf).get();
    // Init
    CData/*3:0*/ __Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__31__Vfuncout;
    __Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__31__Vfuncout = 0;
    SData/*15:0*/ __Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__31__v;
    __Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__31__v = 0;
    CData/*3:0*/ __Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__32__Vfuncout;
    __Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__32__Vfuncout = 0;
    SData/*15:0*/ __Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__32__v;
    __Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__32__v = 0;
    CData/*3:0*/ __Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__33__Vfuncout;
    __Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__33__Vfuncout = 0;
    SData/*15:0*/ __Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__33__v;
    __Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__33__v = 0;
    CData/*3:0*/ __Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__34__Vfuncout;
    __Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__34__Vfuncout = 0;
    SData/*15:0*/ __Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__34__v;
    __Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__34__v = 0;
    // Body
    vlSelfRef.u_core__DOT__u_eg__DOT__i_fire = vlSelfRef.u_core__DOT__eg_fire;
    vlSelfRef.u_core__DOT__u_rq__DOT__i_sel = vlSelfRef.u_core__DOT__hb_sel;
    vlSelfRef.u_core__DOT__u_rq__DOT__i_gclass = vlSelfRef.u_core__DOT__hb_gcl;
    vlSelfRef.u_core__DOT__u_rq__DOT__esel = 0U;
    if ((1U & (IData)(vlSelfRef.u_core__DOT__hb_sel))) {
        vlSelfRef.u_core__DOT__u_rq__DOT__esel = 0U;
    }
    if ((2U & (IData)(vlSelfRef.u_core__DOT__hb_sel))) {
        vlSelfRef.u_core__DOT__u_rq__DOT__esel = 1U;
    }
    if ((4U & (IData)(vlSelfRef.u_core__DOT__hb_sel))) {
        vlSelfRef.u_core__DOT__u_rq__DOT__esel = 2U;
    }
    vlSelfRef.u_rp__DOT__i_myid = vlSelfRef.i_myid;
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__i_sel 
        = (1U & ((IData)(vlSelfRef.u_core__DOT__hb_sel) 
                 >> 0U));
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__i_sel 
        = (1U & ((IData)(vlSelfRef.u_core__DOT__hb_sel) 
                 >> 1U));
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__i_sel 
        = (1U & ((IData)(vlSelfRef.u_core__DOT__hb_sel) 
                 >> 2U));
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__i_sel 
        = (1U & ((IData)(vlSelfRef.u_core__DOT__hb_sel) 
                 >> 3U));
    vlSelfRef.df_wr = vlSelfRef.u_core__DOT__df_wr;
    vlSelfRef.df_addr = vlSelfRef.u_core__DOT__df_addr;
    vlSelfRef.df_wdata = vlSelfRef.u_core__DOT__df_wdata;
    vlSelfRef.u_egbuf__DOT__m_valid = vlSelfRef.u_egbuf__DOT__a_v;
    vlSelfRef.w_act = vlSelfRef.u_core__DOT__act;
    vlSelfRef.u_core__DOT__o_ftrace = vlSelfRef.u_core__DOT__u_eg__DOT__f;
    vlSelfRef.u_core__DOT__u_eg__DOT__o_f = vlSelfRef.u_core__DOT__u_eg__DOT__f;
    vlSelfRef.u_df__DOT__o_eta_f = vlSelfRef.u_df__DOT__dial
        [0U];
    vlSelfRef.d_eta_f = vlSelfRef.u_df__DOT__dial[0U];
    vlSelfRef.u_df__DOT__o_eta_s = vlSelfRef.u_df__DOT__dial
        [1U];
    vlSelfRef.d_eta_s = vlSelfRef.u_df__DOT__dial[1U];
    vlSelfRef.u_df__DOT__o_thresh = vlSelfRef.u_df__DOT__dial
        [5U];
    vlSelfRef.u_df__DOT__o_refr = vlSelfRef.u_df__DOT__dial
        [6U];
    vlSelfRef.u_df__DOT__o_cosmin = vlSelfRef.u_df__DOT__dial
        [7U];
    vlSelfRef.d_cosmin = vlSelfRef.u_df__DOT__dial[7U];
    vlSelfRef.u_df__DOT__o_hl = vlSelfRef.u_df__DOT__dial
        [0xaU];
    vlSelfRef.u_df__DOT__o_floor = vlSelfRef.u_df__DOT__dial
        [0xcU];
    vlSelfRef.lo_valid = vlSelfRef.u_core__DOT__lo_valid;
    vlSelfRef.lx_valid = vlSelfRef.u_core__DOT__lx_valid;
    vlSelfRef.lo_op = vlSelfRef.u_core__DOT__lo_op;
    vlSelfRef.lx_op = vlSelfRef.u_core__DOT__lx_op;
    vlSelfRef.lo_src = vlSelfRef.u_core__DOT__lo_src;
    vlSelfRef.lx_src = vlSelfRef.u_core__DOT__lx_src;
    vlSelfRef.lo_dst = vlSelfRef.u_core__DOT__lo_dst;
    vlSelfRef.lx_dst = vlSelfRef.u_core__DOT__lx_dst;
    vlSelfRef.lo_a0 = vlSelfRef.u_core__DOT__lo_a0;
    vlSelfRef.lx_a0 = vlSelfRef.u_core__DOT__lx_a0;
    vlSelfRef.lo_a1 = vlSelfRef.u_core__DOT__lo_a1;
    vlSelfRef.lx_a1 = vlSelfRef.u_core__DOT__lx_a1;
    vlSelfRef.lo_a2 = vlSelfRef.u_core__DOT__lo_a2;
    vlSelfRef.lx_a2 = vlSelfRef.u_core__DOT__lx_a2;
    vlSelfRef.lo_dat = vlSelfRef.u_core__DOT__lo_dat;
    vlSelfRef.lx_dat = vlSelfRef.u_core__DOT__lx_dat;
    vlSelfRef.u_core__DOT__ci_a0_rsvd = (vlSelfRef.u_inbuf__DOT__a_q[1U] 
                                         >> 0x14U);
    vlSelfRef.u_inbuf__DOT__m_valid = vlSelfRef.u_inbuf__DOT__a_v;
    vlSelfRef.w_bound = vlSelfRef.u_core__DOT__bound;
    vlSelfRef.w_cid = vlSelfRef.u_core__DOT__cell_id;
    vlSelfRef.u_core__DOT__eff_pe = (((QData)((IData)(
                                                      (7U 
                                                       & (- (IData)(
                                                                    (1U 
                                                                     & (IData)(
                                                                               (vlSelfRef.u_core__DOT__eff_p 
                                                                                >> 0x20U)))))))) 
                                      << 0x21U) | vlSelfRef.u_core__DOT__eff_p);
    vlSelfRef.u_core__DOT__prod_p = (0x1ffffffffULL 
                                     & VL_MULS_QQQ(33, 
                                                   (0x1ffffffffULL 
                                                    & VL_EXTENDS_QI(33,17, (IData)(vlSelfRef.u_core__DOT__eff_w))), 
                                                   (0x1ffffffffULL 
                                                    & VL_EXTENDS_QI(33,16, (IData)(vlSelfRef.u_core__DOT__lr_dat)))));
    vlSelfRef.u_inbuf__DOT__pop = ((IData)(vlSelfRef.u_core__DOT__ci_ready) 
                                   & (IData)(vlSelfRef.u_inbuf__DOT__a_v));
    vlSelfRef.li_valid_w = vlSelfRef.u_egbuf__DOT__a_v;
    vlSelfRef.d_thresh = vlSelfRef.u_df__DOT__dial[5U];
    vlSelfRef.d_refr = vlSelfRef.u_df__DOT__dial[6U];
    vlSelfRef.w_ftrace = vlSelfRef.u_core__DOT__u_eg__DOT__f;
    vlSelfRef.u_core__DOT__rq_tick = (2U == (IData)(vlSelfRef.u_core__DOT__hb_cmd));
    vlSelfRef.u_df__DOT__o_kf = (0xfU & vlSelfRef.u_df__DOT__dial
                                 [2U]);
    vlSelfRef.u_df__DOT__o_ks = (0xfU & vlSelfRef.u_df__DOT__dial
                                 [3U]);
    vlSelfRef.u_inbuf__DOT__m_dst = (0xfU & vlSelfRef.u_inbuf__DOT__a_q[2U]);
    vlSelfRef.ci_valid = vlSelfRef.u_inbuf__DOT__a_v;
    vlSelfRef.ci_ready_w = vlSelfRef.u_core__DOT__ci_ready;
    vlSelfRef.df_rd = vlSelfRef.u_core__DOT__df_rd;
    vlSelfRef.df_rdata = vlSelfRef.u_df__DOT__o_rdata;
    vlSelfRef.df_rstb = vlSelfRef.u_df__DOT__o_rstb;
    vlSelfRef.u_core__DOT__eg_tick = (0x11U == (IData)(vlSelfRef.u_core__DOT__state));
    vlSelfRef.df_wr_g = ((IData)(vlSelfRef.i_bdf_wr) 
                         | (IData)(vlSelfRef.u_core__DOT__df_wr));
    vlSelfRef.u_core__DOT__eg_live = ((0U == vlSelfRef.u_df__DOT__dial
                                       [0xcU]) | ((IData)(vlSelfRef.u_core__DOT__u_eg__DOT__f) 
                                                  >= 
                                                  vlSelfRef.u_df__DOT__dial
                                                  [0xcU]));
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__hlc 
        = (0x1ffffU & ((IData)(1U) + (IData)(vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__hl_cnt)));
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__hlc 
        = (0x1ffffU & ((IData)(1U) + (IData)(vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__hl_cnt)));
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__hlc 
        = (0x1ffffU & ((IData)(1U) + (IData)(vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__hl_cnt)));
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__hlc 
        = (0x1ffffU & ((IData)(1U) + (IData)(vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__hl_cnt)));
    if (vlSelfRef.i_bdf_wr) {
        vlSelfRef.df_addr_g = vlSelfRef.i_bdf_addr;
        vlSelfRef.df_wdata_g = vlSelfRef.i_bdf_wdata;
    } else {
        vlSelfRef.df_addr_g = vlSelfRef.u_core__DOT__df_addr;
        vlSelfRef.df_wdata_g = vlSelfRef.u_core__DOT__df_wdata;
    }
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__agen 
        = ((IData)(1U) + vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__age);
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__agen 
        = ((IData)(1U) + vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__age);
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__agen 
        = ((IData)(1U) + vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__age);
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__agen 
        = ((IData)(1U) + vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__age);
    vlSelfRef.ci_op = (7U & (vlSelfRef.u_inbuf__DOT__a_q[2U] 
                             >> 8U));
    vlSelfRef.ci_src = (0xfU & (vlSelfRef.u_inbuf__DOT__a_q[2U] 
                                >> 4U));
    vlSelfRef.ci_a0 = (vlSelfRef.u_inbuf__DOT__a_q[1U] 
                       >> 0x10U);
    vlSelfRef.ci_a1 = (0xffffU & vlSelfRef.u_inbuf__DOT__a_q[1U]);
    vlSelfRef.ci_a2 = (vlSelfRef.u_inbuf__DOT__a_q[0U] 
                       >> 0x10U);
    vlSelfRef.ci_dat = (0xffffU & vlSelfRef.u_inbuf__DOT__a_q[0U]);
    vlSelfRef.u_core__DOT__act_e = (((QData)((IData)(
                                                     (0xfffffU 
                                                      & (- (IData)(
                                                                   (1U 
                                                                    & ((IData)(vlSelfRef.u_core__DOT__act) 
                                                                       >> 0xfU))))))) 
                                     << 0x10U) | (QData)((IData)(vlSelfRef.u_core__DOT__act)));
    vlSelfRef.eg_s_valid = ((IData)(vlSelfRef.u_core__DOT__lo_valid) 
                            | (IData)(vlSelfRef.u_core__DOT__lx_valid));
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__ridx32 
        = vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__ridx;
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__ridx32 
        = vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__ridx;
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__ridx32 
        = vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__ridx;
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__ridx32 
        = vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__ridx;
    vlSelfRef.done_vec = (((IData)(vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__o_done) 
                           << 3U) | (((IData)(vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__o_done) 
                                      << 2U) | (((IData)(vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__o_done) 
                                                 << 1U) 
                                                | (IData)(vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__o_done))));
    vlSelfRef.d_ka = (0xfU & vlSelfRef.u_df__DOT__dial
                      [4U]);
    vlSelfRef.hb_cmd = vlSelfRef.u_core__DOT__hb_cmd;
    vlSelfRef.hb_gcl = vlSelfRef.u_core__DOT__hb_gcl;
    vlSelfRef.d_hl = vlSelfRef.u_df__DOT__dial[0xaU];
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__whs 
        = ((0xffU < (IData)(vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__wh))
            ? 0xffffU : (0xffffU & VL_SHIFTL_III(16,16,32, (IData)(vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__wh), 8U)));
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__whs 
        = ((0xffU < (IData)(vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__wh))
            ? 0xffffU : (0xffffU & VL_SHIFTL_III(16,16,32, (IData)(vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__wh), 8U)));
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__whs 
        = ((0xffU < (IData)(vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__wh))
            ? 0xffffU : (0xffffU & VL_SHIFTL_III(16,16,32, (IData)(vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__wh), 8U)));
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__whs 
        = ((0xffU < (IData)(vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__wh))
            ? 0xffffU : (0xffffU & VL_SHIFTL_III(16,16,32, (IData)(vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__wh), 8U)));
    vlSelfRef.hb_base = vlSelfRef.u_core__DOT__hb_base;
    if (vlSelfRef.u_core__DOT__lo_valid) {
        vlSelfRef.eg_op = vlSelfRef.u_core__DOT__lo_op;
        vlSelfRef.eg_src = vlSelfRef.u_core__DOT__lo_src;
        vlSelfRef.eg_dst = vlSelfRef.u_core__DOT__lo_dst;
        vlSelfRef.eg_a0 = vlSelfRef.u_core__DOT__lo_a0;
        vlSelfRef.eg_a1 = vlSelfRef.u_core__DOT__lo_a1;
        vlSelfRef.eg_a2 = vlSelfRef.u_core__DOT__lo_a2;
        vlSelfRef.eg_dat = vlSelfRef.u_core__DOT__lo_dat;
    } else {
        vlSelfRef.eg_op = vlSelfRef.u_core__DOT__lx_op;
        vlSelfRef.eg_src = vlSelfRef.u_core__DOT__lx_src;
        vlSelfRef.eg_dst = vlSelfRef.u_core__DOT__lx_dst;
        vlSelfRef.eg_a0 = vlSelfRef.u_core__DOT__lx_a0;
        vlSelfRef.eg_a1 = vlSelfRef.u_core__DOT__lx_a1;
        vlSelfRef.eg_a2 = vlSelfRef.u_core__DOT__lx_a2;
        vlSelfRef.eg_dat = vlSelfRef.u_core__DOT__lx_dat;
    }
    vlSelfRef.u_core__DOT__rq_train = (5U == (IData)(vlSelfRef.u_core__DOT__hb_cmd));
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__g_lad_sat__DOT__sat 
        = (1U & (vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__acc 
                 >> 0x10U));
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__g_lad_sat__DOT__sat 
        = (1U & (vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__acc 
                 >> 0x10U));
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__g_lad_sat__DOT__sat 
        = (1U & (vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__acc 
                 >> 0x10U));
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__g_lad_sat__DOT__sat 
        = (1U & (vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__acc 
                 >> 0x10U));
    vlSelfRef.d_kle = (0xfU & vlSelfRef.u_df__DOT__dial
                       [0xbU]);
    __Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__31__v 
        = vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__wh;
    __Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__31__Vfuncout = 0U;
    if ((1U & (IData)(__Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__31__v))) {
        __Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__31__Vfuncout = 0U;
    }
    if ((2U & (IData)(__Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__31__v))) {
        __Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__31__Vfuncout = 1U;
    }
    if ((4U & (IData)(__Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__31__v))) {
        __Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__31__Vfuncout = 2U;
    }
    if ((8U & (IData)(__Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__31__v))) {
        __Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__31__Vfuncout = 3U;
    }
    if ((0x10U & (IData)(__Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__31__v))) {
        __Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__31__Vfuncout = 4U;
    }
    if ((0x20U & (IData)(__Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__31__v))) {
        __Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__31__Vfuncout = 5U;
    }
    if ((0x40U & (IData)(__Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__31__v))) {
        __Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__31__Vfuncout = 6U;
    }
    if ((0x80U & (IData)(__Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__31__v))) {
        __Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__31__Vfuncout = 7U;
    }
    if ((0x100U & (IData)(__Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__31__v))) {
        __Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__31__Vfuncout = 8U;
    }
    if ((0x200U & (IData)(__Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__31__v))) {
        __Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__31__Vfuncout = 9U;
    }
    if ((0x400U & (IData)(__Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__31__v))) {
        __Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__31__Vfuncout = 0xaU;
    }
    if ((0x800U & (IData)(__Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__31__v))) {
        __Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__31__Vfuncout = 0xbU;
    }
    if ((0x1000U & (IData)(__Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__31__v))) {
        __Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__31__Vfuncout = 0xcU;
    }
    if ((0x2000U & (IData)(__Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__31__v))) {
        __Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__31__Vfuncout = 0xdU;
    }
    if ((0x4000U & (IData)(__Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__31__v))) {
        __Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__31__Vfuncout = 0xeU;
    }
    if ((0x8000U & (IData)(__Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__31__v))) {
        __Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__31__Vfuncout = 0xfU;
    }
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__wmsb 
        = __Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__31__Vfuncout;
    __Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__32__v 
        = vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__wh;
    __Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__32__Vfuncout = 0U;
    if ((1U & (IData)(__Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__32__v))) {
        __Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__32__Vfuncout = 0U;
    }
    if ((2U & (IData)(__Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__32__v))) {
        __Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__32__Vfuncout = 1U;
    }
    if ((4U & (IData)(__Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__32__v))) {
        __Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__32__Vfuncout = 2U;
    }
    if ((8U & (IData)(__Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__32__v))) {
        __Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__32__Vfuncout = 3U;
    }
    if ((0x10U & (IData)(__Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__32__v))) {
        __Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__32__Vfuncout = 4U;
    }
    if ((0x20U & (IData)(__Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__32__v))) {
        __Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__32__Vfuncout = 5U;
    }
    if ((0x40U & (IData)(__Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__32__v))) {
        __Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__32__Vfuncout = 6U;
    }
    if ((0x80U & (IData)(__Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__32__v))) {
        __Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__32__Vfuncout = 7U;
    }
    if ((0x100U & (IData)(__Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__32__v))) {
        __Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__32__Vfuncout = 8U;
    }
    if ((0x200U & (IData)(__Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__32__v))) {
        __Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__32__Vfuncout = 9U;
    }
    if ((0x400U & (IData)(__Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__32__v))) {
        __Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__32__Vfuncout = 0xaU;
    }
    if ((0x800U & (IData)(__Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__32__v))) {
        __Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__32__Vfuncout = 0xbU;
    }
    if ((0x1000U & (IData)(__Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__32__v))) {
        __Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__32__Vfuncout = 0xcU;
    }
    if ((0x2000U & (IData)(__Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__32__v))) {
        __Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__32__Vfuncout = 0xdU;
    }
    if ((0x4000U & (IData)(__Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__32__v))) {
        __Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__32__Vfuncout = 0xeU;
    }
    if ((0x8000U & (IData)(__Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__32__v))) {
        __Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__32__Vfuncout = 0xfU;
    }
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__wmsb 
        = __Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__32__Vfuncout;
    __Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__33__v 
        = vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__wh;
    __Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__33__Vfuncout = 0U;
    if ((1U & (IData)(__Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__33__v))) {
        __Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__33__Vfuncout = 0U;
    }
    if ((2U & (IData)(__Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__33__v))) {
        __Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__33__Vfuncout = 1U;
    }
    if ((4U & (IData)(__Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__33__v))) {
        __Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__33__Vfuncout = 2U;
    }
    if ((8U & (IData)(__Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__33__v))) {
        __Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__33__Vfuncout = 3U;
    }
    if ((0x10U & (IData)(__Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__33__v))) {
        __Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__33__Vfuncout = 4U;
    }
    if ((0x20U & (IData)(__Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__33__v))) {
        __Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__33__Vfuncout = 5U;
    }
    if ((0x40U & (IData)(__Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__33__v))) {
        __Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__33__Vfuncout = 6U;
    }
    if ((0x80U & (IData)(__Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__33__v))) {
        __Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__33__Vfuncout = 7U;
    }
    if ((0x100U & (IData)(__Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__33__v))) {
        __Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__33__Vfuncout = 8U;
    }
    if ((0x200U & (IData)(__Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__33__v))) {
        __Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__33__Vfuncout = 9U;
    }
    if ((0x400U & (IData)(__Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__33__v))) {
        __Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__33__Vfuncout = 0xaU;
    }
    if ((0x800U & (IData)(__Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__33__v))) {
        __Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__33__Vfuncout = 0xbU;
    }
    if ((0x1000U & (IData)(__Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__33__v))) {
        __Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__33__Vfuncout = 0xcU;
    }
    if ((0x2000U & (IData)(__Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__33__v))) {
        __Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__33__Vfuncout = 0xdU;
    }
    if ((0x4000U & (IData)(__Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__33__v))) {
        __Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__33__Vfuncout = 0xeU;
    }
    if ((0x8000U & (IData)(__Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__33__v))) {
        __Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__33__Vfuncout = 0xfU;
    }
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__wmsb 
        = __Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__33__Vfuncout;
    __Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__34__v 
        = vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__wh;
    __Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__34__Vfuncout = 0U;
    if ((1U & (IData)(__Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__34__v))) {
        __Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__34__Vfuncout = 0U;
    }
    if ((2U & (IData)(__Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__34__v))) {
        __Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__34__Vfuncout = 1U;
    }
    if ((4U & (IData)(__Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__34__v))) {
        __Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__34__Vfuncout = 2U;
    }
    if ((8U & (IData)(__Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__34__v))) {
        __Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__34__Vfuncout = 3U;
    }
    if ((0x10U & (IData)(__Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__34__v))) {
        __Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__34__Vfuncout = 4U;
    }
    if ((0x20U & (IData)(__Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__34__v))) {
        __Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__34__Vfuncout = 5U;
    }
    if ((0x40U & (IData)(__Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__34__v))) {
        __Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__34__Vfuncout = 6U;
    }
    if ((0x80U & (IData)(__Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__34__v))) {
        __Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__34__Vfuncout = 7U;
    }
    if ((0x100U & (IData)(__Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__34__v))) {
        __Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__34__Vfuncout = 8U;
    }
    if ((0x200U & (IData)(__Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__34__v))) {
        __Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__34__Vfuncout = 9U;
    }
    if ((0x400U & (IData)(__Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__34__v))) {
        __Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__34__Vfuncout = 0xaU;
    }
    if ((0x800U & (IData)(__Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__34__v))) {
        __Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__34__Vfuncout = 0xbU;
    }
    if ((0x1000U & (IData)(__Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__34__v))) {
        __Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__34__Vfuncout = 0xcU;
    }
    if ((0x2000U & (IData)(__Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__34__v))) {
        __Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__34__Vfuncout = 0xdU;
    }
    if ((0x4000U & (IData)(__Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__34__v))) {
        __Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__34__Vfuncout = 0xeU;
    }
    if ((0x8000U & (IData)(__Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__34__v))) {
        __Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__34__Vfuncout = 0xfU;
    }
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__wmsb 
        = __Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__34__Vfuncout;
    vlSelfRef.d_floor = vlSelfRef.u_df__DOT__dial[0xcU];
    vlSelfRef.u_egbuf__DOT__s_ready = (1U & (~ (IData)(vlSelfRef.u_egbuf__DOT__b_v)));
    vlSelfRef.d_qleak = (0xfU & vlSelfRef.u_df__DOT__dial
                         [0xfU]);
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__hlth 
        = vlSelfRef.u_df__DOT__dial[0xaU];
    vlSelfRef.hb_sel = vlSelfRef.u_core__DOT__hb_sel;
    vlSelfRef.ovf_vec = (((IData)(vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__o_ovf) 
                          << 3U) | (((IData)(vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__o_ovf) 
                                     << 2U) | (((IData)(vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__o_ovf) 
                                                << 1U) 
                                               | (IData)(vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__o_ovf))));
    vlSelfRef.w_flat = (((QData)((IData)(vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__o_w)) 
                         << 0x30U) | (((QData)((IData)(
                                                       (((IData)(vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__o_w) 
                                                         << 0x10U) 
                                                        | (IData)(vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__o_w)))) 
                                       << 0x10U) | (QData)((IData)(vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__o_w))));
    vlSelfRef.li_op_w = (7U & (vlSelfRef.u_egbuf__DOT__a_q[2U] 
                               >> 8U));
    vlSelfRef.li_src_w = (0xfU & (vlSelfRef.u_egbuf__DOT__a_q[2U] 
                                  >> 4U));
    vlSelfRef.li_dst_w = (0xfU & vlSelfRef.u_egbuf__DOT__a_q[2U]);
    vlSelfRef.li_a0_w = (vlSelfRef.u_egbuf__DOT__a_q[1U] 
                         >> 0x10U);
    vlSelfRef.li_a1_w = (0xffffU & vlSelfRef.u_egbuf__DOT__a_q[1U]);
    vlSelfRef.li_a2_w = (vlSelfRef.u_egbuf__DOT__a_q[0U] 
                         >> 0x10U);
    vlSelfRef.li_dat_w = (0xffffU & vlSelfRef.u_egbuf__DOT__a_q[0U]);
    vlSelfRef.d_rqen = (1U & (vlSelfRef.u_df__DOT__dial
                              [0xeU] >> 0xfU));
    vlSelfRef.d_mode = (1U & vlSelfRef.u_df__DOT__dial
                        [9U]);
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__gcl 
        = ((8U <= (IData)(vlSelfRef.u_core__DOT__hb_gcl))
            ? 7U : (IData)(vlSelfRef.u_core__DOT__hb_gcl));
    vlSelfRef.d_p0e = (0x1fU & vlSelfRef.u_df__DOT__dial
                       [8U]);
    vlSelfRef.u_core__DOT__u_rq__DOT__rsel = 0U;
    if ((1U & (IData)(vlSelfRef.u_core__DOT__hb_sel))) {
        vlSelfRef.u_core__DOT__u_rq__DOT__rsel = vlSelfRef.u_core__DOT__u_rq__DOT__R
            [0U];
    }
    if ((2U & (IData)(vlSelfRef.u_core__DOT__hb_sel))) {
        vlSelfRef.u_core__DOT__u_rq__DOT__rsel = vlSelfRef.u_core__DOT__u_rq__DOT__R
            [1U];
    }
    if ((4U & (IData)(vlSelfRef.u_core__DOT__hb_sel))) {
        vlSelfRef.u_core__DOT__u_rq__DOT__rsel = vlSelfRef.u_core__DOT__u_rq__DOT__R
            [2U];
    }
    if ((8U & (IData)(vlSelfRef.u_core__DOT__hb_sel))) {
        vlSelfRef.u_core__DOT__u_rq__DOT__esel = 3U;
        vlSelfRef.u_core__DOT__u_rq__DOT__rsel = vlSelfRef.u_core__DOT__u_rq__DOT__R
            [3U];
    }
    vlSelfRef.d_qdw = (0xfU & vlSelfRef.u_df__DOT__dial
                       [0xeU]);
    vlSelfRef.ld_ready = (1U & (~ (IData)(vlSelfRef.u_inbuf__DOT__b_v)));
    vlSelfRef.u_df__DOT__rst_n = vlSelfRef.i_por_n;
    vlSelfRef.u_inbuf__DOT__rst_n = vlSelfRef.rst_n;
    vlSelfRef.u_egbuf__DOT__rst_n = vlSelfRef.rst_n;
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__rst_n 
        = vlSelfRef.rst_n;
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__rst_n 
        = vlSelfRef.rst_n;
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__rst_n 
        = vlSelfRef.rst_n;
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__rst_n 
        = vlSelfRef.rst_n;
    vlSelfRef.u_core__DOT__rst_n = vlSelfRef.rst_n;
    vlSelfRef.u_df__DOT__clk = vlSelfRef.clk;
    vlSelfRef.u_inbuf__DOT__clk = vlSelfRef.clk;
    vlSelfRef.u_egbuf__DOT__clk = vlSelfRef.clk;
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__clk 
        = vlSelfRef.clk;
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__clk 
        = vlSelfRef.clk;
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__clk 
        = vlSelfRef.clk;
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__clk 
        = vlSelfRef.clk;
    vlSelfRef.u_core__DOT__clk = vlSelfRef.clk;
    vlSelfRef.u_rp__DOT__ri_valid = vlSelfRef.ri_valid;
    vlSelfRef.u_rp__DOT__ro_ready = vlSelfRef.ro_ready;
    vlSelfRef.u_rp__DOT__ri_op = vlSelfRef.ri_op;
    vlSelfRef.u_rp__DOT__ld_op = vlSelfRef.ri_op;
    vlSelfRef.ld_op = vlSelfRef.ri_op;
    vlSelfRef.u_rp__DOT__ri_src = vlSelfRef.ri_src;
    vlSelfRef.u_rp__DOT__ld_src = vlSelfRef.ri_src;
    vlSelfRef.ld_src = vlSelfRef.ri_src;
    vlSelfRef.u_rp__DOT__ri_a0 = vlSelfRef.ri_a0;
    vlSelfRef.u_rp__DOT__ld_a0 = vlSelfRef.ri_a0;
    vlSelfRef.ld_a0 = vlSelfRef.ri_a0;
    vlSelfRef.u_rp__DOT__ri_a1 = vlSelfRef.ri_a1;
    vlSelfRef.u_rp__DOT__ld_a1 = vlSelfRef.ri_a1;
    vlSelfRef.ld_a1 = vlSelfRef.ri_a1;
    vlSelfRef.u_rp__DOT__ri_a2 = vlSelfRef.ri_a2;
    vlSelfRef.u_rp__DOT__ld_a2 = vlSelfRef.ri_a2;
    vlSelfRef.ld_a2 = vlSelfRef.ri_a2;
    vlSelfRef.u_rp__DOT__ri_dat = vlSelfRef.ri_dat;
    vlSelfRef.u_rp__DOT__ld_dat = vlSelfRef.ri_dat;
    vlSelfRef.ld_dat = vlSelfRef.ri_dat;
    vlSelfRef.u_core__DOT__s_tick = vlSelfRef.s_tick;
    vlSelfRef.u_rp__DOT__ri_dst = vlSelfRef.ri_dst;
    vlSelfRef.u_rp__DOT__ld_dst = vlSelfRef.ri_dst;
    vlSelfRef.w_lddst = vlSelfRef.ri_dst;
    vlSelfRef.u_inbuf__DOT__s_bus[0U] = (IData)((((QData)((IData)(vlSelfRef.ri_a0)) 
                                                  << 0x30U) 
                                                 | (((QData)((IData)(
                                                                     (((IData)(vlSelfRef.ri_a1) 
                                                                       << 0x10U) 
                                                                      | (IData)(vlSelfRef.ri_a2)))) 
                                                     << 0x10U) 
                                                    | (QData)((IData)(vlSelfRef.ri_dat)))));
    vlSelfRef.u_inbuf__DOT__s_bus[1U] = (IData)(((((QData)((IData)(vlSelfRef.ri_a0)) 
                                                   << 0x30U) 
                                                  | (((QData)((IData)(
                                                                      (((IData)(vlSelfRef.ri_a1) 
                                                                        << 0x10U) 
                                                                       | (IData)(vlSelfRef.ri_a2)))) 
                                                      << 0x10U) 
                                                     | (QData)((IData)(vlSelfRef.ri_dat)))) 
                                                 >> 0x20U));
    vlSelfRef.u_inbuf__DOT__s_bus[2U] = (((IData)(vlSelfRef.ri_op) 
                                          << 8U) | 
                                         (((IData)(vlSelfRef.ri_src) 
                                           << 4U) | (IData)(vlSelfRef.ri_dst)));
    vlSelfRef.ld_valid = ((IData)(vlSelfRef.ri_valid) 
                          & ((IData)(vlSelfRef.i_myid) 
                             == (IData)(vlSelfRef.ri_dst)));
    vlSelfRef.u_rp__DOT__li_valid = vlSelfRef.li_valid_w;
    vlSelfRef.u_core__DOT__d_thresh = vlSelfRef.d_thresh;
    vlSelfRef.u_core__DOT__d_refr = vlSelfRef.d_refr;
    vlSelfRef.u_df__DOT__i_probe = vlSelfRef.w_ftrace;
    vlSelfRef.u_core__DOT__u_rq__DOT__i_tick = vlSelfRef.u_core__DOT__rq_tick;
    vlSelfRef.d_kf = vlSelfRef.u_df__DOT__o_kf;
    vlSelfRef.d_ks = vlSelfRef.u_df__DOT__o_ks;
    vlSelfRef.w_indst = vlSelfRef.u_inbuf__DOT__m_dst;
    vlSelfRef.u_core__DOT__ci_valid = vlSelfRef.ci_valid;
    vlSelfRef.u_inbuf__DOT__m_ready = vlSelfRef.ci_ready_w;
    vlSelfRef.u_df__DOT__i_rd = vlSelfRef.df_rd;
    vlSelfRef.u_core__DOT__df_rdata = vlSelfRef.df_rdata;
    vlSelfRef.u_core__DOT__df_rstb = vlSelfRef.df_rstb;
    vlSelfRef.u_core__DOT__u_eg__DOT__i_tick = vlSelfRef.u_core__DOT__eg_tick;
    vlSelfRef.u_df__DOT__i_wr = vlSelfRef.df_wr_g;
    vlSelfRef.u_core__DOT__u_eg__DOT__o_live = vlSelfRef.u_core__DOT__eg_live;
    vlSelfRef.u_df__DOT__i_addr = vlSelfRef.df_addr_g;
    vlSelfRef.u_df__DOT__i_wdata = vlSelfRef.df_wdata_g;
    vlSelfRef.u_core__DOT__ci_op = vlSelfRef.ci_op;
    vlSelfRef.u_inbuf__DOT__m_op = vlSelfRef.ci_op;
    vlSelfRef.u_core__DOT__ci_src = vlSelfRef.ci_src;
    vlSelfRef.u_inbuf__DOT__m_src = vlSelfRef.ci_src;
    vlSelfRef.u_core__DOT__ci_a0 = vlSelfRef.ci_a0;
    vlSelfRef.u_inbuf__DOT__m_a0 = vlSelfRef.ci_a0;
    vlSelfRef.u_core__DOT__ci_a1 = vlSelfRef.ci_a1;
    vlSelfRef.u_inbuf__DOT__m_a1 = vlSelfRef.ci_a1;
    vlSelfRef.u_core__DOT__ci_a2 = vlSelfRef.ci_a2;
    vlSelfRef.u_inbuf__DOT__m_a2 = vlSelfRef.ci_a2;
    vlSelfRef.u_core__DOT__ci_dat = vlSelfRef.ci_dat;
    vlSelfRef.u_inbuf__DOT__m_dat = vlSelfRef.ci_dat;
    vlSelfRef.u_egbuf__DOT__s_valid = vlSelfRef.eg_s_valid;
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__rsh 
        = ((IData)(8U) - vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__ridx32);
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__rsh 
        = ((IData)(8U) - vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__ridx32);
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__rsh 
        = ((IData)(8U) - vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__ridx32);
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__rsh 
        = ((IData)(8U) - vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__ridx32);
    vlSelfRef.hb_done = (0U != (IData)(vlSelfRef.done_vec));
    vlSelfRef.u_core__DOT__d_ka = vlSelfRef.d_ka;
    vlSelfRef.u_df__DOT__o_ka = vlSelfRef.d_ka;
    vlSelfRef.u_core__DOT__leak_sum = (0xfffffffffULL 
                                       & (vlSelfRef.u_core__DOT__act_e 
                                          - VL_SHIFTRS_QQI(36,36,4, vlSelfRef.u_core__DOT__act_e, (IData)(vlSelfRef.d_ka))));
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__i_cmd 
        = vlSelfRef.hb_cmd;
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__i_cmd 
        = vlSelfRef.hb_cmd;
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__i_cmd 
        = vlSelfRef.hb_cmd;
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__i_cmd 
        = vlSelfRef.hb_cmd;
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__i_gclass 
        = vlSelfRef.hb_gcl;
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__i_gclass 
        = vlSelfRef.hb_gcl;
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__i_gclass 
        = vlSelfRef.hb_gcl;
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__i_gclass 
        = vlSelfRef.hb_gcl;
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__i_hl 
        = vlSelfRef.d_hl;
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__i_hl 
        = vlSelfRef.d_hl;
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__i_hl 
        = vlSelfRef.d_hl;
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__i_hl 
        = vlSelfRef.d_hl;
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__i_base 
        = vlSelfRef.hb_base;
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__i_base 
        = vlSelfRef.hb_base;
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__i_base 
        = vlSelfRef.hb_base;
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__i_base 
        = vlSelfRef.hb_base;
    vlSelfRef.u_egbuf__DOT__s_op = vlSelfRef.eg_op;
    vlSelfRef.u_egbuf__DOT__s_src = vlSelfRef.eg_src;
    vlSelfRef.u_egbuf__DOT__s_dst = vlSelfRef.eg_dst;
    vlSelfRef.u_egbuf__DOT__s_a0 = vlSelfRef.eg_a0;
    vlSelfRef.u_egbuf__DOT__s_a1 = vlSelfRef.eg_a1;
    vlSelfRef.u_egbuf__DOT__s_a2 = vlSelfRef.eg_a2;
    vlSelfRef.u_egbuf__DOT__s_dat = vlSelfRef.eg_dat;
    vlSelfRef.u_egbuf__DOT__s_bus[0U] = (IData)((((QData)((IData)(vlSelfRef.eg_a0)) 
                                                  << 0x30U) 
                                                 | (((QData)((IData)(
                                                                     (((IData)(vlSelfRef.eg_a1) 
                                                                       << 0x10U) 
                                                                      | (IData)(vlSelfRef.eg_a2)))) 
                                                     << 0x10U) 
                                                    | (QData)((IData)(vlSelfRef.eg_dat)))));
    vlSelfRef.u_egbuf__DOT__s_bus[1U] = (IData)(((((QData)((IData)(vlSelfRef.eg_a0)) 
                                                   << 0x30U) 
                                                  | (((QData)((IData)(
                                                                      (((IData)(vlSelfRef.eg_a1) 
                                                                        << 0x10U) 
                                                                       | (IData)(vlSelfRef.eg_a2)))) 
                                                      << 0x10U) 
                                                     | (QData)((IData)(vlSelfRef.eg_dat)))) 
                                                 >> 0x20U));
    vlSelfRef.u_egbuf__DOT__s_bus[2U] = (((IData)(vlSelfRef.eg_op) 
                                          << 8U) | 
                                         (((IData)(vlSelfRef.eg_src) 
                                           << 4U) | (IData)(vlSelfRef.eg_dst)));
    vlSelfRef.u_core__DOT__u_rq__DOT__i_train = vlSelfRef.u_core__DOT__rq_train;
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__lad 
        = ((IData)(vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__g_lad_sat__DOT__sat)
            ? 0xffffU : (0xffffU & vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__acc));
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__lad 
        = ((IData)(vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__g_lad_sat__DOT__sat)
            ? 0xffffU : (0xffffU & vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__acc));
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__lad 
        = ((IData)(vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__g_lad_sat__DOT__sat)
            ? 0xffffU : (0xffffU & vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__acc));
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__lad 
        = ((IData)(vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__g_lad_sat__DOT__sat)
            ? 0xffffU : (0xffffU & vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__acc));
    vlSelfRef.u_df__DOT__o_kle = vlSelfRef.d_kle;
    vlSelfRef.u_core__DOT__d_kle = vlSelfRef.d_kle;
    vlSelfRef.u_core__DOT__u_eg__DOT__fleak = (0xffffU 
                                               & ((IData)(vlSelfRef.u_core__DOT__u_eg__DOT__f) 
                                                  - 
                                                  ((IData)(vlSelfRef.u_core__DOT__u_eg__DOT__f) 
                                                   >> (IData)(vlSelfRef.d_kle))));
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__shl2 
        = (0x1fU & ((IData)(vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__wmsb) 
                    + (IData)(vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__wmsb)));
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__shl2 
        = (0x1fU & ((IData)(vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__wmsb) 
                    + (IData)(vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__wmsb)));
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__shl2 
        = (0x1fU & ((IData)(vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__wmsb) 
                    + (IData)(vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__wmsb)));
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__shl2 
        = (0x1fU & ((IData)(vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__wmsb) 
                    + (IData)(vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__wmsb)));
    vlSelfRef.u_core__DOT__d_floor = vlSelfRef.d_floor;
    vlSelfRef.u_core__DOT__u_eg__DOT__o_gclass = ((
                                                   (0U 
                                                    == (IData)(vlSelfRef.d_floor)) 
                                                   | (0U 
                                                      == (IData)(vlSelfRef.u_core__DOT__u_eg__DOT__f)))
                                                   ? 0U
                                                   : 
                                                  (0xfU 
                                                   & ((IData)(0xfU) 
                                                      - 
                                                      ([&]() {
                        vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__30__v 
                            = vlSelfRef.u_core__DOT__u_eg__DOT__f;
                        vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__30__Vfuncout = 0U;
                        if ((1U & (IData)(vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__30__v))) {
                            vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__30__Vfuncout = 0U;
                        }
                        vlSelfRef.u_core__DOT__u_eg__DOT__msb_idx__Vstatic__j = 1U;
                        if ((2U & (IData)(vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__30__v))) {
                            vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__30__Vfuncout = 1U;
                        }
                        vlSelfRef.u_core__DOT__u_eg__DOT__msb_idx__Vstatic__j = 2U;
                        if ((4U & (IData)(vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__30__v))) {
                            vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__30__Vfuncout = 2U;
                        }
                        vlSelfRef.u_core__DOT__u_eg__DOT__msb_idx__Vstatic__j = 3U;
                        if ((8U & (IData)(vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__30__v))) {
                            vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__30__Vfuncout = 3U;
                        }
                        vlSelfRef.u_core__DOT__u_eg__DOT__msb_idx__Vstatic__j = 4U;
                        if ((0x10U & (IData)(vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__30__v))) {
                            vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__30__Vfuncout = 4U;
                        }
                        vlSelfRef.u_core__DOT__u_eg__DOT__msb_idx__Vstatic__j = 5U;
                        if ((0x20U & (IData)(vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__30__v))) {
                            vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__30__Vfuncout = 5U;
                        }
                        vlSelfRef.u_core__DOT__u_eg__DOT__msb_idx__Vstatic__j = 6U;
                        if ((0x40U & (IData)(vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__30__v))) {
                            vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__30__Vfuncout = 6U;
                        }
                        vlSelfRef.u_core__DOT__u_eg__DOT__msb_idx__Vstatic__j = 7U;
                        if ((0x80U & (IData)(vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__30__v))) {
                            vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__30__Vfuncout = 7U;
                        }
                        vlSelfRef.u_core__DOT__u_eg__DOT__msb_idx__Vstatic__j = 8U;
                        if ((0x100U & (IData)(vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__30__v))) {
                            vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__30__Vfuncout = 8U;
                        }
                        vlSelfRef.u_core__DOT__u_eg__DOT__msb_idx__Vstatic__j = 9U;
                        if ((0x200U & (IData)(vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__30__v))) {
                            vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__30__Vfuncout = 9U;
                        }
                        vlSelfRef.u_core__DOT__u_eg__DOT__msb_idx__Vstatic__j = 0xaU;
                        if ((0x400U & (IData)(vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__30__v))) {
                            vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__30__Vfuncout = 0xaU;
                        }
                        vlSelfRef.u_core__DOT__u_eg__DOT__msb_idx__Vstatic__j = 0xbU;
                        if ((0x800U & (IData)(vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__30__v))) {
                            vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__30__Vfuncout = 0xbU;
                        }
                        vlSelfRef.u_core__DOT__u_eg__DOT__msb_idx__Vstatic__j = 0xcU;
                        if ((0x1000U & (IData)(vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__30__v))) {
                            vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__30__Vfuncout = 0xcU;
                        }
                        vlSelfRef.u_core__DOT__u_eg__DOT__msb_idx__Vstatic__j = 0xdU;
                        if ((0x2000U & (IData)(vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__30__v))) {
                            vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__30__Vfuncout = 0xdU;
                        }
                        vlSelfRef.u_core__DOT__u_eg__DOT__msb_idx__Vstatic__j = 0xeU;
                        if ((0x4000U & (IData)(vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__30__v))) {
                            vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__30__Vfuncout = 0xeU;
                        }
                        vlSelfRef.u_core__DOT__u_eg__DOT__msb_idx__Vstatic__j = 0xfU;
                        if ((0x8000U & (IData)(vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__30__v))) {
                            vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__30__Vfuncout = 0xfU;
                        }
                        vlSelfRef.u_core__DOT__u_eg__DOT__msb_idx__Vstatic__j = 0x10U;
                    }(), (IData)(vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__30__Vfuncout)))));
    vlSelfRef.eg_s_ready = vlSelfRef.u_egbuf__DOT__s_ready;
    vlSelfRef.u_egbuf__DOT__push = ((IData)(vlSelfRef.u_egbuf__DOT__s_ready) 
                                    & (IData)(vlSelfRef.eg_s_valid));
    vlSelfRef.lo_grant = (1U & ((~ (IData)(vlSelfRef.u_core__DOT__lo_valid)) 
                                | (IData)(vlSelfRef.u_egbuf__DOT__s_ready)));
    vlSelfRef.lx_grant = ((~ (IData)(vlSelfRef.u_core__DOT__lo_valid)) 
                          & (IData)(vlSelfRef.u_egbuf__DOT__s_ready));
    vlSelfRef.u_df__DOT__o_qleak = vlSelfRef.d_qleak;
    vlSelfRef.u_core__DOT__d_qleak = vlSelfRef.d_qleak;
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__hlth 
        = vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__hlth;
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__hlth 
        = vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__hlth;
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__hlth 
        = vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__hlth;
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__hlend 
        = (vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__hlc 
           >= vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__hlth);
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__hlend 
        = (vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__hlc 
           >= vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__hlth);
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__hlend 
        = (vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__hlc 
           >= vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__hlth);
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__hlend 
        = (vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__hlc 
           >= vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__hlth);
    vlSelfRef.o_ovf = (0U != (IData)(vlSelfRef.ovf_vec));
    vlSelfRef.hb_w_mux = 0U;
    if ((1U & (IData)(vlSelfRef.hb_sel))) {
        vlSelfRef.hb_w_mux = (0xffffU & (IData)(vlSelfRef.w_flat));
    }
    if ((2U & (IData)(vlSelfRef.hb_sel))) {
        vlSelfRef.hb_w_mux = (0xffffU & (IData)((vlSelfRef.w_flat 
                                                 >> 0x10U)));
    }
    if ((4U & (IData)(vlSelfRef.hb_sel))) {
        vlSelfRef.hb_w_mux = (0xffffU & (IData)((vlSelfRef.w_flat 
                                                 >> 0x20U)));
    }
    if ((8U & (IData)(vlSelfRef.hb_sel))) {
        vlSelfRef.hb_w_mux = (0xffffU & (IData)((vlSelfRef.w_flat 
                                                 >> 0x30U)));
    }
    vlSelfRef.u_rp__DOT__li_op = vlSelfRef.li_op_w;
    vlSelfRef.u_egbuf__DOT__m_op = vlSelfRef.li_op_w;
    vlSelfRef.u_rp__DOT__li_src = vlSelfRef.li_src_w;
    vlSelfRef.u_egbuf__DOT__m_src = vlSelfRef.li_src_w;
    vlSelfRef.u_rp__DOT__li_dst = vlSelfRef.li_dst_w;
    vlSelfRef.u_egbuf__DOT__m_dst = vlSelfRef.li_dst_w;
    vlSelfRef.u_rp__DOT__li_a0 = vlSelfRef.li_a0_w;
    vlSelfRef.u_egbuf__DOT__m_a0 = vlSelfRef.li_a0_w;
    vlSelfRef.u_rp__DOT__li_a1 = vlSelfRef.li_a1_w;
    vlSelfRef.u_egbuf__DOT__m_a1 = vlSelfRef.li_a1_w;
    vlSelfRef.u_rp__DOT__li_a2 = vlSelfRef.li_a2_w;
    vlSelfRef.u_egbuf__DOT__m_a2 = vlSelfRef.li_a2_w;
    vlSelfRef.u_rp__DOT__li_dat = vlSelfRef.li_dat_w;
    vlSelfRef.u_egbuf__DOT__m_dat = vlSelfRef.li_dat_w;
    vlSelfRef.u_df__DOT__o_rqen = vlSelfRef.d_rqen;
    vlSelfRef.u_core__DOT__d_rqen = vlSelfRef.d_rqen;
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__i_mode 
        = vlSelfRef.d_mode;
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__i_mode 
        = vlSelfRef.d_mode;
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__i_mode 
        = vlSelfRef.d_mode;
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__i_mode 
        = vlSelfRef.d_mode;
    vlSelfRef.u_df__DOT__o_mode = vlSelfRef.d_mode;
    vlSelfRef.u_core__DOT__u_rq__DOT__gcl = vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__gcl;
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__gcl 
        = vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__gcl;
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__gcl 
        = vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__gcl;
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__gcl 
        = vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__gcl;
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__i_p0e 
        = vlSelfRef.d_p0e;
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__i_p0e 
        = vlSelfRef.d_p0e;
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__i_p0e 
        = vlSelfRef.d_p0e;
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__i_p0e 
        = vlSelfRef.d_p0e;
    vlSelfRef.u_df__DOT__o_p0e = vlSelfRef.d_p0e;
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__p0 
        = ((IData)(1U) << (IData)(vlSelfRef.d_p0e));
    vlSelfRef.u_core__DOT__u_rq__DOT__rleak = (0xffffU 
                                               & ((IData)(vlSelfRef.u_core__DOT__u_rq__DOT__rsel) 
                                                  - 
                                                  ((IData)(vlSelfRef.u_core__DOT__u_rq__DOT__rsel) 
                                                   >> (IData)(vlSelfRef.d_qleak))));
    vlSelfRef.u_df__DOT__o_qdw = vlSelfRef.d_qdw;
    vlSelfRef.u_core__DOT__d_qdw = vlSelfRef.d_qdw;
    vlSelfRef.u_core__DOT__u_rq__DOT__cred_cur = ((IData)(vlSelfRef.u_core__DOT__u_rq__DOT__rsel) 
                                                  >> (IData)(vlSelfRef.d_qdw));
    vlSelfRef.u_core__DOT__u_rq__DOT__dsh = (0x3fU 
                                             & (((IData)(8U) 
                                                 + (IData)(vlSelfRef.d_qdw)) 
                                                - (IData)(vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__gcl)));
    vlSelfRef.u_rp__DOT__ld_ready = vlSelfRef.ld_ready;
    vlSelfRef.u_inbuf__DOT__s_ready = vlSelfRef.ld_ready;
    vlSelfRef.u_core__DOT__u_eg__DOT__rst_n = vlSelfRef.u_core__DOT__rst_n;
    vlSelfRef.u_core__DOT__u_rq__DOT__rst_n = vlSelfRef.u_core__DOT__rst_n;
    vlSelfRef.u_core__DOT__u_eg__DOT__clk = vlSelfRef.u_core__DOT__clk;
    vlSelfRef.u_core__DOT__u_rq__DOT__clk = vlSelfRef.u_core__DOT__clk;
    vlSelfRef.u_inbuf__DOT__s_op = vlSelfRef.ld_op;
    vlSelfRef.u_inbuf__DOT__s_src = vlSelfRef.ld_src;
    vlSelfRef.u_inbuf__DOT__s_a0 = vlSelfRef.ld_a0;
    vlSelfRef.u_inbuf__DOT__s_a1 = vlSelfRef.ld_a1;
    vlSelfRef.u_inbuf__DOT__s_a2 = vlSelfRef.ld_a2;
    vlSelfRef.u_inbuf__DOT__s_dat = vlSelfRef.ld_dat;
    vlSelfRef.u_inbuf__DOT__s_dst = vlSelfRef.w_lddst;
    if (vlSelfRef.ld_valid) {
        vlSelfRef.u_inbuf__DOT__s_valid = 1U;
        vlSelfRef.u_rp__DOT__ld_valid = 1U;
        vlSelfRef.u_rp__DOT__hit = 1U;
        vlSelfRef.u_rp__DOT__ri_ready = vlSelfRef.ld_ready;
        vlSelfRef.u_inbuf__DOT__push = vlSelfRef.ld_ready;
    } else {
        vlSelfRef.u_inbuf__DOT__s_valid = 0U;
        vlSelfRef.u_rp__DOT__ld_valid = 0U;
        vlSelfRef.u_rp__DOT__hit = 0U;
        vlSelfRef.u_rp__DOT__ri_ready = vlSelfRef.ro_ready;
        vlSelfRef.u_inbuf__DOT__push = 0U;
    }
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__addw 
        = (0x1ffffU & VL_SHIFTL_III(17,17,32, vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__c
                                    [(7U & (IData)(vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__ridx))], vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__rsh));
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__addw 
        = (0x1ffffU & VL_SHIFTL_III(17,17,32, vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__c
                                    [(7U & (IData)(vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__ridx))], vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__rsh));
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__addw 
        = (0x1ffffU & VL_SHIFTL_III(17,17,32, vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__c
                                    [(7U & (IData)(vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__ridx))], vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__rsh));
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__addw 
        = (0x1ffffU & VL_SHIFTL_III(17,17,32, vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__c
                                    [(7U & (IData)(vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__ridx))], vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__rsh));
    vlSelfRef.u_core__DOT__hb_done = vlSelfRef.hb_done;
    if (vlSelfRef.d_mode) {
        vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__eng 
            = vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__whs;
        vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__eng 
            = vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__whs;
        vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__eng 
            = vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__whs;
        vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__eng 
            = vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__whs;
    } else {
        vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__eng 
            = vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__lad;
        vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__eng 
            = vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__lad;
        vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__eng 
            = vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__lad;
        vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__eng 
            = vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__lad;
    }
    vlSelfRef.u_core__DOT__u_eg__DOT__i_kle = vlSelfRef.u_core__DOT__d_kle;
    vlSelfRef.u_core__DOT__u_eg__DOT__fsnap = (((IData)(vlSelfRef.u_core__DOT__u_eg__DOT__fleak) 
                                                <= 
                                                vlSelfRef.u_df__DOT__dial
                                                [0xcU]) 
                                               | ((1U 
                                                   >= (IData)(vlSelfRef.u_core__DOT__u_eg__DOT__fleak)) 
                                                  | ((IData)(vlSelfRef.u_core__DOT__u_eg__DOT__fleak) 
                                                     >= (IData)(vlSelfRef.u_core__DOT__u_eg__DOT__f))));
    vlSelfRef.u_core__DOT__u_eg__DOT__i_floor = vlSelfRef.u_core__DOT__d_floor;
    vlSelfRef.u_core__DOT__eg_gclass = vlSelfRef.u_core__DOT__u_eg__DOT__o_gclass;
    vlSelfRef.u_core__DOT__lo_ready = vlSelfRef.lo_grant;
    vlSelfRef.u_core__DOT__lx_ready = vlSelfRef.lx_grant;
    vlSelfRef.u_core__DOT__u_rq__DOT__i_qleak = vlSelfRef.u_core__DOT__d_qleak;
    vlSelfRef.hb_w = vlSelfRef.hb_w_mux;
    vlSelfRef.u_core__DOT__u_rq__DOT__i_en = vlSelfRef.u_core__DOT__d_rqen;
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__p0 
        = vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__p0;
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__p0 
        = vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__p0;
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__p0 
        = vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__p0;
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__ivr 
        = (vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__p0 
           >> (IData)(vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__shl2));
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__ivr 
        = (vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__p0 
           >> (IData)(vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__shl2));
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__ivr 
        = (vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__p0 
           >> (IData)(vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__shl2));
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__ivr 
        = (vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__p0 
           >> (IData)(vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__shl2));
    vlSelfRef.u_core__DOT__u_rq__DOT__rsnap = ((1U 
                                                >= (IData)(vlSelfRef.u_core__DOT__u_rq__DOT__rleak)) 
                                               | ((IData)(vlSelfRef.u_core__DOT__u_rq__DOT__rleak) 
                                                  >= (IData)(vlSelfRef.u_core__DOT__u_rq__DOT__rsel)));
    vlSelfRef.u_core__DOT__u_rq__DOT__i_qdw = vlSelfRef.u_core__DOT__d_qdw;
    vlSelfRef.u_core__DOT__rq_credit = ((IData)(vlSelfRef.d_rqen)
                                         ? (0xffffU 
                                            & vlSelfRef.u_core__DOT__u_rq__DOT__cred_cur)
                                         : 0U);
    vlSelfRef.u_core__DOT__u_rq__DOT__qbase = VL_SHIFTL_III(32,32,6, (IData)(1U), (IData)(vlSelfRef.u_core__DOT__u_rq__DOT__dsh));
    vlSelfRef.ri_ready = vlSelfRef.u_rp__DOT__ri_ready;
    vlSelfRef.u_rp__DOT__consumed = vlSelfRef.u_inbuf__DOT__push;
    vlSelfRef.u_rp__DOT__inject_ok = (1U & ((~ (IData)(vlSelfRef.ri_valid)) 
                                            | (IData)(vlSelfRef.u_inbuf__DOT__push)));
    vlSelfRef.u_rp__DOT__transit = ((~ (IData)(vlSelfRef.u_inbuf__DOT__push)) 
                                    & (IData)(vlSelfRef.ri_valid));
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__wfin 
        = (0x1ffffU & ((IData)(vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__base) 
                       + (IData)(vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__eng)));
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__wfin 
        = (0x1ffffU & ((IData)(vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__base) 
                       + (IData)(vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__eng)));
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__wfin 
        = (0x1ffffU & ((IData)(vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__base) 
                       + (IData)(vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__eng)));
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__wfin 
        = (0x1ffffU & ((IData)(vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__base) 
                       + (IData)(vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__eng)));
    vlSelfRef.u_core__DOT__hb_w = vlSelfRef.hb_w;
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__ival 
        = ((0U == vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__ivr)
            ? 1U : vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__ivr);
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__ival 
        = ((0U == vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__ivr)
            ? 1U : vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__ivr);
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__ival 
        = ((0U == vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__ivr)
            ? 1U : vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__ivr);
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__ival 
        = ((0U == vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__ivr)
            ? 1U : vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__ivr);
    vlSelfRef.u_core__DOT__u_rq__DOT__rleakn = ((IData)(vlSelfRef.u_core__DOT__u_rq__DOT__rsnap)
                                                 ? 0U
                                                 : (IData)(vlSelfRef.u_core__DOT__u_rq__DOT__rleak));
    vlSelfRef.u_core__DOT__u_rq__DOT__o_credit = vlSelfRef.u_core__DOT__rq_credit;
    vlSelfRef.u_core__DOT__w_rq = (0x1ffffU & ((IData)(vlSelfRef.hb_w_mux) 
                                               + (IData)(vlSelfRef.u_core__DOT__rq_credit)));
    vlSelfRef.u_core__DOT__u_rq__DOT__dep = (VL_SHIFTR_III(32,32,32, vlSelfRef.u_core__DOT__u_rq__DOT__qbase, 2U) 
                                             + VL_SHIFTR_III(32,32,32, vlSelfRef.u_core__DOT__u_rq__DOT__qbase, 5U));
    vlSelfRef.li_ready_w = ((IData)(vlSelfRef.u_rp__DOT__inject_ok) 
                            & (IData)(vlSelfRef.ro_ready));
    vlSelfRef.u_rp__DOT__ro_valid = ((IData)(vlSelfRef.u_rp__DOT__transit) 
                                     | ((IData)(vlSelfRef.u_egbuf__DOT__a_v) 
                                        & (IData)(vlSelfRef.u_rp__DOT__inject_ok)));
    if (vlSelfRef.u_rp__DOT__transit) {
        vlSelfRef.u_rp__DOT__ro_op = vlSelfRef.ri_op;
        vlSelfRef.u_rp__DOT__ro_src = vlSelfRef.ri_src;
        vlSelfRef.u_rp__DOT__ro_dst = vlSelfRef.ri_dst;
        vlSelfRef.u_rp__DOT__ro_a0 = vlSelfRef.ri_a0;
        vlSelfRef.u_rp__DOT__ro_a1 = vlSelfRef.ri_a1;
        vlSelfRef.u_rp__DOT__ro_a2 = vlSelfRef.ri_a2;
        vlSelfRef.u_rp__DOT__ro_dat = vlSelfRef.ri_dat;
    } else {
        vlSelfRef.u_rp__DOT__ro_op = vlSelfRef.li_op_w;
        vlSelfRef.u_rp__DOT__ro_src = vlSelfRef.li_src_w;
        vlSelfRef.u_rp__DOT__ro_dst = vlSelfRef.li_dst_w;
        vlSelfRef.u_rp__DOT__ro_a0 = vlSelfRef.li_a0_w;
        vlSelfRef.u_rp__DOT__ro_a1 = vlSelfRef.li_a1_w;
        vlSelfRef.u_rp__DOT__ro_a2 = vlSelfRef.li_a2_w;
        vlSelfRef.u_rp__DOT__ro_dat = vlSelfRef.li_dat_w;
    }
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__wout 
        = ((0x10000U & vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__wfin)
            ? 0xffffU : (0xffffU & vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__wfin));
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__wout 
        = ((0x10000U & vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__wfin)
            ? 0xffffU : (0xffffU & vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__wfin));
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__wout 
        = ((0x10000U & vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__wfin)
            ? 0xffffU : (0xffffU & vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__wfin));
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__wout 
        = ((0x10000U & vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__wfin)
            ? 0xffffU : (0xffffU & vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__wfin));
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__decn 
        = ((0U != (IData)(vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__wh)) 
           & (vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__agen 
              >= vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__ival));
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__decn 
        = ((0U != (IData)(vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__wh)) 
           & (vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__agen 
              >= vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__ival));
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__decn 
        = ((0U != (IData)(vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__wh)) 
           & (vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__agen 
              >= vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__ival));
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__decn 
        = ((0U != (IData)(vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__wh)) 
           & (vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__agen 
              >= vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__ival));
    vlSelfRef.u_core__DOT__hb_wq = ((0x10000U & vlSelfRef.u_core__DOT__w_rq)
                                     ? 0xffffU : (0xffffU 
                                                  & vlSelfRef.u_core__DOT__w_rq));
    vlSelfRef.u_core__DOT__u_rq__DOT__rsum = (0x1ffffffffULL 
                                              & ((QData)((IData)(vlSelfRef.u_core__DOT__u_rq__DOT__rsel)) 
                                                 + (QData)((IData)(vlSelfRef.u_core__DOT__u_rq__DOT__dep))));
    vlSelfRef.u_egbuf__DOT__m_ready = vlSelfRef.li_ready_w;
    vlSelfRef.u_rp__DOT__li_ready = vlSelfRef.li_ready_w;
    vlSelfRef.u_egbuf__DOT__pop = ((IData)(vlSelfRef.u_egbuf__DOT__a_v) 
                                   & (IData)(vlSelfRef.li_ready_w));
    vlSelfRef.ro_valid = vlSelfRef.u_rp__DOT__ro_valid;
    vlSelfRef.ro_op = vlSelfRef.u_rp__DOT__ro_op;
    vlSelfRef.ro_src = vlSelfRef.u_rp__DOT__ro_src;
    vlSelfRef.ro_dst = vlSelfRef.u_rp__DOT__ro_dst;
    vlSelfRef.ro_a0 = vlSelfRef.u_rp__DOT__ro_a0;
    vlSelfRef.ro_a1 = vlSelfRef.u_rp__DOT__ro_a1;
    vlSelfRef.ro_a2 = vlSelfRef.u_rp__DOT__ro_a2;
    vlSelfRef.ro_dat = vlSelfRef.u_rp__DOT__ro_dat;
    vlSelfRef.u_core__DOT__prod = (0x1ffffffffULL & 
                                   VL_MULS_QQQ(33, 
                                               (0x1ffffffffULL 
                                                & VL_EXTENDS_QI(33,17, (IData)(vlSelfRef.u_core__DOT__hb_wq))), 
                                               (0x1ffffffffULL 
                                                & VL_EXTENDS_QI(33,16, (IData)(vlSelfRef.u_core__DOT__lr_dat)))));
    vlSelfRef.u_core__DOT__u_rq__DOT__rsat = (vlSelfRef.u_core__DOT__u_rq__DOT__rsum 
                                              > vlSelfRef.u_core__DOT__u_rq__DOT__rfull);
    vlSelfRef.u_core__DOT__prod_e = (((QData)((IData)(
                                                      (7U 
                                                       & (- (IData)(
                                                                    (1U 
                                                                     & (IData)(
                                                                               (vlSelfRef.u_core__DOT__prod 
                                                                                >> 0x20U)))))))) 
                                      << 0x21U) | vlSelfRef.u_core__DOT__prod);
    vlSelfRef.u_core__DOT__u_rq__DOT__rdepn = ((IData)(vlSelfRef.u_core__DOT__u_rq__DOT__rsat)
                                                ? 0xffffU
                                                : (0xffffU 
                                                   & (IData)(vlSelfRef.u_core__DOT__u_rq__DOT__rsum)));
    vlSelfRef.u_core__DOT__eff_sum = (0xfffffffffULL 
                                      & (vlSelfRef.u_core__DOT__act_e 
                                         + VL_SHIFTRS_QQI(36,36,32, vlSelfRef.u_core__DOT__prod_e, 0xfU)));
    vlSelfRef.u_core__DOT__u_rq__DOT__cred_new = ((IData)(vlSelfRef.u_core__DOT__u_rq__DOT__rdepn) 
                                                  >> (IData)(vlSelfRef.d_qdw));
    vlSelfRef.u_core__DOT__u_rq__DOT__o_antic = ((IData)(vlSelfRef.d_rqen) 
                                                 & ((IData)(vlSelfRef.u_core__DOT__rq_train) 
                                                    & (vlSelfRef.u_core__DOT__u_rq__DOT__cred_new 
                                                       > vlSelfRef.u_core__DOT__u_rq__DOT__cred_cur)));
    vlSelfRef.u_core__DOT__o_antic = vlSelfRef.u_core__DOT__u_rq__DOT__o_antic;
    vlSelfRef.w_antic = vlSelfRef.u_core__DOT__u_rq__DOT__o_antic;
}

VL_INLINE_OPT void Vq_fabric_top_q_cell___nba_sequent__TOP__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__connc__DOT__u_cell__0(Vq_fabric_top_q_cell* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    Vq_fabric_top__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vq_fabric_top_q_cell___nba_sequent__TOP__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__connc__DOT__u_cell__0\n"); );
    auto &vlSelfRef = std::ref(*vlSelf).get();
    // Init
    SData/*15:0*/ __Vfunc_u_core__DOT__sclip16__28__Vfuncout;
    __Vfunc_u_core__DOT__sclip16__28__Vfuncout = 0;
    QData/*35:0*/ __Vfunc_u_core__DOT__sclip16__28__v;
    __Vfunc_u_core__DOT__sclip16__28__v = 0;
    SData/*15:0*/ __Vfunc_u_core__DOT__sclip16__29__Vfuncout;
    __Vfunc_u_core__DOT__sclip16__29__Vfuncout = 0;
    QData/*35:0*/ __Vfunc_u_core__DOT__sclip16__29__v;
    __Vfunc_u_core__DOT__sclip16__29__v = 0;
    CData/*3:0*/ __Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__31__Vfuncout;
    __Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__31__Vfuncout = 0;
    SData/*15:0*/ __Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__31__v;
    __Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__31__v = 0;
    CData/*3:0*/ __Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__32__Vfuncout;
    __Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__32__Vfuncout = 0;
    SData/*15:0*/ __Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__32__v;
    __Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__32__v = 0;
    CData/*3:0*/ __Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__33__Vfuncout;
    __Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__33__Vfuncout = 0;
    SData/*15:0*/ __Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__33__v;
    __Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__33__v = 0;
    CData/*3:0*/ __Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__34__Vfuncout;
    __Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__34__Vfuncout = 0;
    SData/*15:0*/ __Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__34__v;
    __Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__34__v = 0;
    CData/*0:0*/ __Vdly__u_core__DOT__lo_valid;
    __Vdly__u_core__DOT__lo_valid = 0;
    CData/*0:0*/ __Vdly__u_core__DOT__lx_valid;
    __Vdly__u_core__DOT__lx_valid = 0;
    CData/*4:0*/ __Vdly__u_core__DOT__state;
    __Vdly__u_core__DOT__state = 0;
    SData/*15:0*/ __Vdly__u_core__DOT__act;
    __Vdly__u_core__DOT__act = 0;
    CData/*0:0*/ __Vdly__u_core__DOT__ci_ready;
    __Vdly__u_core__DOT__ci_ready = 0;
    SData/*15:0*/ __Vdly__u_core__DOT__refr;
    __Vdly__u_core__DOT__refr = 0;
    CData/*2:0*/ __Vdly__u_core__DOT__eidx;
    __Vdly__u_core__DOT__eidx = 0;
    IData/*18:0*/ __Vdly__u_core__DOT__wacc;
    __Vdly__u_core__DOT__wacc = 0;
    CData/*0:0*/ __Vdly__u_core__DOT__tick_pend;
    __Vdly__u_core__DOT__tick_pend = 0;
    CData/*0:0*/ __Vdly__u_inbuf__DOT__a_v;
    __Vdly__u_inbuf__DOT__a_v = 0;
    CData/*0:0*/ __Vdly__u_egbuf__DOT__a_v;
    __Vdly__u_egbuf__DOT__a_v = 0;
    SData/*15:0*/ __Vdly__edges__BRA__0__KET____DOT__u_hebb__DOT__wh;
    __Vdly__edges__BRA__0__KET____DOT__u_hebb__DOT__wh = 0;
    IData/*23:0*/ __Vdly__edges__BRA__0__KET____DOT__u_hebb__DOT__age;
    __Vdly__edges__BRA__0__KET____DOT__u_hebb__DOT__age = 0;
    SData/*15:0*/ __Vdly__edges__BRA__0__KET____DOT__u_hebb__DOT__hl_cnt;
    __Vdly__edges__BRA__0__KET____DOT__u_hebb__DOT__hl_cnt = 0;
    SData/*15:0*/ __Vdly__edges__BRA__1__KET____DOT__u_hebb__DOT__wh;
    __Vdly__edges__BRA__1__KET____DOT__u_hebb__DOT__wh = 0;
    IData/*23:0*/ __Vdly__edges__BRA__1__KET____DOT__u_hebb__DOT__age;
    __Vdly__edges__BRA__1__KET____DOT__u_hebb__DOT__age = 0;
    SData/*15:0*/ __Vdly__edges__BRA__1__KET____DOT__u_hebb__DOT__hl_cnt;
    __Vdly__edges__BRA__1__KET____DOT__u_hebb__DOT__hl_cnt = 0;
    SData/*15:0*/ __Vdly__edges__BRA__2__KET____DOT__u_hebb__DOT__wh;
    __Vdly__edges__BRA__2__KET____DOT__u_hebb__DOT__wh = 0;
    IData/*23:0*/ __Vdly__edges__BRA__2__KET____DOT__u_hebb__DOT__age;
    __Vdly__edges__BRA__2__KET____DOT__u_hebb__DOT__age = 0;
    SData/*15:0*/ __Vdly__edges__BRA__2__KET____DOT__u_hebb__DOT__hl_cnt;
    __Vdly__edges__BRA__2__KET____DOT__u_hebb__DOT__hl_cnt = 0;
    SData/*15:0*/ __Vdly__edges__BRA__3__KET____DOT__u_hebb__DOT__wh;
    __Vdly__edges__BRA__3__KET____DOT__u_hebb__DOT__wh = 0;
    IData/*23:0*/ __Vdly__edges__BRA__3__KET____DOT__u_hebb__DOT__age;
    __Vdly__edges__BRA__3__KET____DOT__u_hebb__DOT__age = 0;
    SData/*15:0*/ __Vdly__edges__BRA__3__KET____DOT__u_hebb__DOT__hl_cnt;
    __Vdly__edges__BRA__3__KET____DOT__u_hebb__DOT__hl_cnt = 0;
    CData/*3:0*/ __VdlyVal__u_core__DOT__etab__v0;
    __VdlyVal__u_core__DOT__etab__v0 = 0;
    CData/*1:0*/ __VdlyDim0__u_core__DOT__etab__v0;
    __VdlyDim0__u_core__DOT__etab__v0 = 0;
    CData/*0:0*/ __VdlySet__u_core__DOT__etab__v0;
    __VdlySet__u_core__DOT__etab__v0 = 0;
    CData/*1:0*/ __VdlyDim0__u_core__DOT__ev__v0;
    __VdlyDim0__u_core__DOT__ev__v0 = 0;
    CData/*0:0*/ __VdlySet__u_core__DOT__etab__v1;
    __VdlySet__u_core__DOT__etab__v1 = 0;
    SData/*15:0*/ __VdlyVal__u_core__DOT__u_rq__DOT__R__v0;
    __VdlyVal__u_core__DOT__u_rq__DOT__R__v0 = 0;
    CData/*1:0*/ __VdlyDim0__u_core__DOT__u_rq__DOT__R__v0;
    __VdlyDim0__u_core__DOT__u_rq__DOT__R__v0 = 0;
    CData/*0:0*/ __VdlySet__u_core__DOT__u_rq__DOT__R__v0;
    __VdlySet__u_core__DOT__u_rq__DOT__R__v0 = 0;
    SData/*15:0*/ __VdlyVal__u_core__DOT__u_rq__DOT__R__v1;
    __VdlyVal__u_core__DOT__u_rq__DOT__R__v1 = 0;
    CData/*1:0*/ __VdlyDim0__u_core__DOT__u_rq__DOT__R__v1;
    __VdlyDim0__u_core__DOT__u_rq__DOT__R__v1 = 0;
    CData/*0:0*/ __VdlySet__u_core__DOT__u_rq__DOT__R__v1;
    __VdlySet__u_core__DOT__u_rq__DOT__R__v1 = 0;
    CData/*0:0*/ __VdlySet__u_core__DOT__u_rq__DOT__R__v2;
    __VdlySet__u_core__DOT__u_rq__DOT__R__v2 = 0;
    SData/*15:0*/ __VdlyVal__u_df__DOT__dial__v0;
    __VdlyVal__u_df__DOT__dial__v0 = 0;
    CData/*3:0*/ __VdlyDim0__u_df__DOT__dial__v0;
    __VdlyDim0__u_df__DOT__dial__v0 = 0;
    CData/*0:0*/ __VdlySet__u_df__DOT__dial__v0;
    __VdlySet__u_df__DOT__dial__v0 = 0;
    CData/*0:0*/ __VdlySet__u_df__DOT__dial__v1;
    __VdlySet__u_df__DOT__dial__v1 = 0;
    CData/*7:0*/ __VdlyVal__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v0;
    __VdlyVal__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v0 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v0;
    __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v0 = 0;
    CData/*7:0*/ __VdlyVal__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v1;
    __VdlyVal__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v1 = 0;
    CData/*2:0*/ __VdlyDim0__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v1;
    __VdlyDim0__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v1 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v1;
    __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v1 = 0;
    CData/*7:0*/ __VdlyVal__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v2;
    __VdlyVal__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v2 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v2;
    __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v2 = 0;
    CData/*7:0*/ __VdlyVal__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v3;
    __VdlyVal__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v3 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v3;
    __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v3 = 0;
    CData/*7:0*/ __VdlyVal__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v4;
    __VdlyVal__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v4 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v4;
    __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v4 = 0;
    CData/*7:0*/ __VdlyVal__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v5;
    __VdlyVal__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v5 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v5;
    __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v5 = 0;
    CData/*7:0*/ __VdlyVal__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v6;
    __VdlyVal__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v6 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v6;
    __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v6 = 0;
    CData/*7:0*/ __VdlyVal__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v7;
    __VdlyVal__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v7 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v7;
    __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v7 = 0;
    CData/*7:0*/ __VdlyVal__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v8;
    __VdlyVal__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v8 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v8;
    __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v8 = 0;
    CData/*7:0*/ __VdlyVal__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v10;
    __VdlyVal__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v10 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v10;
    __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v10 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v11;
    __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v11 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v12;
    __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v12 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v13;
    __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v13 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v14;
    __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v14 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v15;
    __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v15 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v16;
    __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v16 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v17;
    __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v17 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v18;
    __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v18 = 0;
    CData/*7:0*/ __VdlyVal__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v0;
    __VdlyVal__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v0 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v0;
    __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v0 = 0;
    CData/*7:0*/ __VdlyVal__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v1;
    __VdlyVal__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v1 = 0;
    CData/*2:0*/ __VdlyDim0__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v1;
    __VdlyDim0__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v1 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v1;
    __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v1 = 0;
    CData/*7:0*/ __VdlyVal__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v2;
    __VdlyVal__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v2 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v2;
    __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v2 = 0;
    CData/*7:0*/ __VdlyVal__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v3;
    __VdlyVal__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v3 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v3;
    __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v3 = 0;
    CData/*7:0*/ __VdlyVal__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v4;
    __VdlyVal__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v4 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v4;
    __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v4 = 0;
    CData/*7:0*/ __VdlyVal__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v5;
    __VdlyVal__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v5 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v5;
    __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v5 = 0;
    CData/*7:0*/ __VdlyVal__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v6;
    __VdlyVal__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v6 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v6;
    __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v6 = 0;
    CData/*7:0*/ __VdlyVal__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v7;
    __VdlyVal__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v7 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v7;
    __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v7 = 0;
    CData/*7:0*/ __VdlyVal__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v8;
    __VdlyVal__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v8 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v8;
    __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v8 = 0;
    CData/*7:0*/ __VdlyVal__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v10;
    __VdlyVal__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v10 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v10;
    __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v10 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v11;
    __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v11 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v12;
    __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v12 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v13;
    __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v13 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v14;
    __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v14 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v15;
    __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v15 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v16;
    __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v16 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v17;
    __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v17 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v18;
    __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v18 = 0;
    CData/*7:0*/ __VdlyVal__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v0;
    __VdlyVal__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v0 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v0;
    __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v0 = 0;
    CData/*7:0*/ __VdlyVal__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v1;
    __VdlyVal__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v1 = 0;
    CData/*2:0*/ __VdlyDim0__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v1;
    __VdlyDim0__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v1 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v1;
    __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v1 = 0;
    CData/*7:0*/ __VdlyVal__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v2;
    __VdlyVal__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v2 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v2;
    __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v2 = 0;
    CData/*7:0*/ __VdlyVal__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v3;
    __VdlyVal__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v3 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v3;
    __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v3 = 0;
    CData/*7:0*/ __VdlyVal__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v4;
    __VdlyVal__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v4 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v4;
    __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v4 = 0;
    CData/*7:0*/ __VdlyVal__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v5;
    __VdlyVal__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v5 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v5;
    __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v5 = 0;
    CData/*7:0*/ __VdlyVal__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v6;
    __VdlyVal__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v6 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v6;
    __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v6 = 0;
    CData/*7:0*/ __VdlyVal__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v7;
    __VdlyVal__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v7 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v7;
    __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v7 = 0;
    CData/*7:0*/ __VdlyVal__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v8;
    __VdlyVal__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v8 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v8;
    __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v8 = 0;
    CData/*7:0*/ __VdlyVal__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v10;
    __VdlyVal__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v10 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v10;
    __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v10 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v11;
    __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v11 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v12;
    __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v12 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v13;
    __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v13 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v14;
    __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v14 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v15;
    __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v15 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v16;
    __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v16 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v17;
    __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v17 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v18;
    __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v18 = 0;
    CData/*7:0*/ __VdlyVal__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v0;
    __VdlyVal__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v0 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v0;
    __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v0 = 0;
    CData/*7:0*/ __VdlyVal__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v1;
    __VdlyVal__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v1 = 0;
    CData/*2:0*/ __VdlyDim0__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v1;
    __VdlyDim0__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v1 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v1;
    __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v1 = 0;
    CData/*7:0*/ __VdlyVal__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v2;
    __VdlyVal__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v2 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v2;
    __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v2 = 0;
    CData/*7:0*/ __VdlyVal__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v3;
    __VdlyVal__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v3 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v3;
    __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v3 = 0;
    CData/*7:0*/ __VdlyVal__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v4;
    __VdlyVal__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v4 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v4;
    __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v4 = 0;
    CData/*7:0*/ __VdlyVal__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v5;
    __VdlyVal__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v5 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v5;
    __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v5 = 0;
    CData/*7:0*/ __VdlyVal__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v6;
    __VdlyVal__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v6 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v6;
    __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v6 = 0;
    CData/*7:0*/ __VdlyVal__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v7;
    __VdlyVal__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v7 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v7;
    __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v7 = 0;
    CData/*7:0*/ __VdlyVal__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v8;
    __VdlyVal__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v8 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v8;
    __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v8 = 0;
    CData/*7:0*/ __VdlyVal__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v10;
    __VdlyVal__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v10 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v10;
    __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v10 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v11;
    __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v11 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v12;
    __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v12 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v13;
    __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v13 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v14;
    __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v14 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v15;
    __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v15 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v16;
    __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v16 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v17;
    __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v17 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v18;
    __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v18 = 0;
    // Body
    __Vdly__u_core__DOT__tick_pend = vlSelfRef.u_core__DOT__tick_pend;
    __Vdly__u_egbuf__DOT__a_v = vlSelfRef.u_egbuf__DOT__a_v;
    __VdlySet__u_core__DOT__u_rq__DOT__R__v0 = 0U;
    __VdlySet__u_core__DOT__u_rq__DOT__R__v1 = 0U;
    __VdlySet__u_core__DOT__u_rq__DOT__R__v2 = 0U;
    __Vdly__u_inbuf__DOT__a_v = vlSelfRef.u_inbuf__DOT__a_v;
    __Vdly__u_core__DOT__refr = vlSelfRef.u_core__DOT__refr;
    __Vdly__u_core__DOT__eidx = vlSelfRef.u_core__DOT__eidx;
    __Vdly__u_core__DOT__wacc = vlSelfRef.u_core__DOT__wacc;
    __Vdly__u_core__DOT__state = vlSelfRef.u_core__DOT__state;
    __VdlySet__u_core__DOT__etab__v0 = 0U;
    __VdlySet__u_core__DOT__etab__v1 = 0U;
    __Vdly__u_core__DOT__ci_ready = vlSelfRef.u_core__DOT__ci_ready;
    __Vdly__u_core__DOT__lx_valid = vlSelfRef.u_core__DOT__lx_valid;
    __Vdly__u_core__DOT__act = vlSelfRef.u_core__DOT__act;
    __Vdly__u_core__DOT__lo_valid = vlSelfRef.u_core__DOT__lo_valid;
    __VdlySet__u_df__DOT__dial__v0 = 0U;
    __VdlySet__u_df__DOT__dial__v1 = 0U;
    __Vdly__edges__BRA__1__KET____DOT__u_hebb__DOT__hl_cnt 
        = vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__hl_cnt;
    __Vdly__edges__BRA__2__KET____DOT__u_hebb__DOT__hl_cnt 
        = vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__hl_cnt;
    __Vdly__edges__BRA__3__KET____DOT__u_hebb__DOT__hl_cnt 
        = vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__hl_cnt;
    __Vdly__edges__BRA__1__KET____DOT__u_hebb__DOT__age 
        = vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__age;
    __Vdly__edges__BRA__2__KET____DOT__u_hebb__DOT__age 
        = vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__age;
    __Vdly__edges__BRA__3__KET____DOT__u_hebb__DOT__age 
        = vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__age;
    __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v0 = 0U;
    __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v1 = 0U;
    __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v2 = 0U;
    __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v3 = 0U;
    __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v4 = 0U;
    __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v5 = 0U;
    __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v6 = 0U;
    __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v7 = 0U;
    __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v8 = 0U;
    __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v10 = 0U;
    __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v11 = 0U;
    __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v12 = 0U;
    __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v13 = 0U;
    __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v14 = 0U;
    __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v15 = 0U;
    __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v16 = 0U;
    __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v17 = 0U;
    __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v18 = 0U;
    __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v0 = 0U;
    __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v1 = 0U;
    __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v2 = 0U;
    __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v3 = 0U;
    __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v4 = 0U;
    __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v5 = 0U;
    __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v6 = 0U;
    __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v7 = 0U;
    __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v8 = 0U;
    __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v10 = 0U;
    __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v11 = 0U;
    __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v12 = 0U;
    __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v13 = 0U;
    __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v14 = 0U;
    __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v15 = 0U;
    __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v16 = 0U;
    __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v17 = 0U;
    __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v18 = 0U;
    __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v0 = 0U;
    __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v1 = 0U;
    __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v2 = 0U;
    __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v3 = 0U;
    __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v4 = 0U;
    __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v5 = 0U;
    __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v6 = 0U;
    __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v7 = 0U;
    __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v8 = 0U;
    __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v10 = 0U;
    __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v11 = 0U;
    __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v12 = 0U;
    __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v13 = 0U;
    __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v14 = 0U;
    __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v15 = 0U;
    __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v16 = 0U;
    __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v17 = 0U;
    __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v18 = 0U;
    __Vdly__edges__BRA__1__KET____DOT__u_hebb__DOT__wh 
        = vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__wh;
    __Vdly__edges__BRA__2__KET____DOT__u_hebb__DOT__wh 
        = vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__wh;
    __Vdly__edges__BRA__3__KET____DOT__u_hebb__DOT__wh 
        = vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__wh;
    __Vdly__edges__BRA__0__KET____DOT__u_hebb__DOT__hl_cnt 
        = vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__hl_cnt;
    __Vdly__edges__BRA__0__KET____DOT__u_hebb__DOT__age 
        = vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__age;
    __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v0 = 0U;
    __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v1 = 0U;
    __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v2 = 0U;
    __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v3 = 0U;
    __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v4 = 0U;
    __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v5 = 0U;
    __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v6 = 0U;
    __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v7 = 0U;
    __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v8 = 0U;
    __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v10 = 0U;
    __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v11 = 0U;
    __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v12 = 0U;
    __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v13 = 0U;
    __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v14 = 0U;
    __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v15 = 0U;
    __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v16 = 0U;
    __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v17 = 0U;
    __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v18 = 0U;
    __Vdly__edges__BRA__0__KET____DOT__u_hebb__DOT__wh 
        = vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__wh;
    if ((1U & (~ (IData)(vlSelfRef.rst_n)))) {
        vlSelfRef.u_core__DOT__i = 1U;
        vlSelfRef.u_core__DOT__i = 2U;
        vlSelfRef.u_core__DOT__i = 3U;
        vlSelfRef.u_core__DOT__i = 4U;
        vlSelfRef.u_core__DOT__u_rq__DOT__j = 1U;
        vlSelfRef.u_core__DOT__u_rq__DOT__j = 2U;
        vlSelfRef.u_core__DOT__u_rq__DOT__j = 3U;
        vlSelfRef.u_core__DOT__u_rq__DOT__j = 4U;
    }
    if (vlSelfRef.rst_n) {
        if (vlSelfRef.s_tick) {
            __Vdly__u_core__DOT__tick_pend = 1U;
        } else if (((2U == (IData)(vlSelfRef.u_core__DOT__state)) 
                    & (IData)(vlSelfRef.u_core__DOT__tick_pend))) {
            __Vdly__u_core__DOT__tick_pend = 0U;
        }
        if (vlSelfRef.d_rqen) {
            if (vlSelfRef.u_core__DOT__rq_train) {
                __VdlyVal__u_core__DOT__u_rq__DOT__R__v0 
                    = vlSelfRef.u_core__DOT__u_rq__DOT__rdepn;
                __VdlyDim0__u_core__DOT__u_rq__DOT__R__v0 
                    = vlSelfRef.u_core__DOT__u_rq__DOT__esel;
                __VdlySet__u_core__DOT__u_rq__DOT__R__v0 = 1U;
            } else if (vlSelfRef.u_core__DOT__rq_tick) {
                __VdlyVal__u_core__DOT__u_rq__DOT__R__v1 
                    = vlSelfRef.u_core__DOT__u_rq__DOT__rleakn;
                __VdlyDim0__u_core__DOT__u_rq__DOT__R__v1 
                    = vlSelfRef.u_core__DOT__u_rq__DOT__esel;
                __VdlySet__u_core__DOT__u_rq__DOT__R__v1 = 1U;
            }
        }
        if (vlSelfRef.u_egbuf__DOT__pop) {
            __Vdly__u_egbuf__DOT__a_v = vlSelfRef.u_egbuf__DOT__b_v;
            vlSelfRef.u_egbuf__DOT__a_q[0U] = vlSelfRef.u_egbuf__DOT__b_q[0U];
            vlSelfRef.u_egbuf__DOT__a_q[1U] = vlSelfRef.u_egbuf__DOT__b_q[1U];
            vlSelfRef.u_egbuf__DOT__a_q[2U] = vlSelfRef.u_egbuf__DOT__b_q[2U];
            vlSelfRef.u_egbuf__DOT__b_v = 0U;
        }
        if (vlSelfRef.u_egbuf__DOT__push) {
            if (((IData)(vlSelfRef.u_egbuf__DOT__a_v) 
                 & (~ (IData)(vlSelfRef.u_egbuf__DOT__pop)))) {
                vlSelfRef.u_egbuf__DOT__b_q[0U] = vlSelfRef.u_egbuf__DOT__s_bus[0U];
                vlSelfRef.u_egbuf__DOT__b_q[1U] = vlSelfRef.u_egbuf__DOT__s_bus[1U];
                vlSelfRef.u_egbuf__DOT__b_q[2U] = vlSelfRef.u_egbuf__DOT__s_bus[2U];
                vlSelfRef.u_egbuf__DOT__b_v = 1U;
            } else {
                vlSelfRef.u_egbuf__DOT__a_q[0U] = vlSelfRef.u_egbuf__DOT__s_bus[0U];
                vlSelfRef.u_egbuf__DOT__a_q[1U] = vlSelfRef.u_egbuf__DOT__s_bus[1U];
                vlSelfRef.u_egbuf__DOT__a_q[2U] = vlSelfRef.u_egbuf__DOT__s_bus[2U];
                __Vdly__u_egbuf__DOT__a_v = 1U;
            }
        }
        if (vlSelfRef.u_inbuf__DOT__pop) {
            __Vdly__u_inbuf__DOT__a_v = vlSelfRef.u_inbuf__DOT__b_v;
            vlSelfRef.u_inbuf__DOT__a_q[0U] = vlSelfRef.u_inbuf__DOT__b_q[0U];
            vlSelfRef.u_inbuf__DOT__a_q[1U] = vlSelfRef.u_inbuf__DOT__b_q[1U];
            vlSelfRef.u_inbuf__DOT__a_q[2U] = vlSelfRef.u_inbuf__DOT__b_q[2U];
            vlSelfRef.u_inbuf__DOT__b_v = 0U;
        }
        if (vlSelfRef.u_inbuf__DOT__push) {
            if (((IData)(vlSelfRef.u_inbuf__DOT__a_v) 
                 & (~ (IData)(vlSelfRef.u_inbuf__DOT__pop)))) {
                vlSelfRef.u_inbuf__DOT__b_q[0U] = vlSelfRef.u_inbuf__DOT__s_bus[0U];
                vlSelfRef.u_inbuf__DOT__b_q[1U] = vlSelfRef.u_inbuf__DOT__s_bus[1U];
                vlSelfRef.u_inbuf__DOT__b_q[2U] = vlSelfRef.u_inbuf__DOT__s_bus[2U];
                vlSelfRef.u_inbuf__DOT__b_v = 1U;
            } else {
                vlSelfRef.u_inbuf__DOT__a_q[0U] = vlSelfRef.u_inbuf__DOT__s_bus[0U];
                vlSelfRef.u_inbuf__DOT__a_q[1U] = vlSelfRef.u_inbuf__DOT__s_bus[1U];
                vlSelfRef.u_inbuf__DOT__a_q[2U] = vlSelfRef.u_inbuf__DOT__s_bus[2U];
                __Vdly__u_inbuf__DOT__a_v = 1U;
            }
        }
        if (vlSelfRef.u_core__DOT__eg_fire) {
            vlSelfRef.u_core__DOT__u_eg__DOT__f = 0xffffU;
        } else if (vlSelfRef.u_core__DOT__eg_tick) {
            vlSelfRef.u_core__DOT__u_eg__DOT__f = ((IData)(vlSelfRef.u_core__DOT__u_eg__DOT__fsnap)
                                                    ? 0U
                                                    : (IData)(vlSelfRef.u_core__DOT__u_eg__DOT__fleak));
        }
        vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__o_done = 0U;
        if (vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__rstate) {
            if ((8U == (IData)(vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__ridx))) {
                vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__o_w 
                    = vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__wout;
                vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__o_done = 1U;
                vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__rstate = 0U;
            } else {
                vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__acc 
                    = (0x1ffffU & (vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__acc 
                                   + vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__addw));
                vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__ridx 
                    = (0x1fU & ((IData)(1U) + (IData)(vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__ridx)));
            }
        } else if ((2U & (IData)(vlSelfRef.u_core__DOT__hb_sel))) {
            if ((4U & (IData)(vlSelfRef.hb_cmd))) {
                if ((1U & (~ ((IData)(vlSelfRef.hb_cmd) 
                              >> 1U)))) {
                    if ((1U & (IData)(vlSelfRef.hb_cmd))) {
                        if (vlSelfRef.d_mode) {
                            if ((0xffffU == (IData)(vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__wh))) {
                                vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__o_ovf = 1U;
                            } else {
                                __Vdly__edges__BRA__1__KET____DOT__u_hebb__DOT__wh 
                                    = (0xffffU & ((IData)(1U) 
                                                  + (IData)(vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__wh)));
                            }
                        } else if ((8U <= (IData)(vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__gcl))) {
                            if ((0xffU == vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__c
                                 [7U])) {
                                vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__o_ovf = 1U;
                            } else {
                                __VdlyVal__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v0 
                                    = (0xffU & ((IData)(1U) 
                                                + vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__c
                                                [7U]));
                                __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v0 = 1U;
                            }
                        } else if ((0xffU == vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__c
                                    [(7U & (IData)(vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__gcl))])) {
                            vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__o_ovf = 1U;
                        } else {
                            __VdlyVal__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v1 
                                = (0xffU & ((IData)(1U) 
                                            + vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__c
                                            [(7U & (IData)(vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__gcl))]));
                            __VdlyDim0__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v1 
                                = (7U & (IData)(vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__gcl));
                            __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v1 = 1U;
                        }
                        vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__o_done = 1U;
                    } else {
                        vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__base 
                            = vlSelfRef.hb_base;
                        vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__o_done = 1U;
                    }
                }
            } else if ((2U & (IData)(vlSelfRef.hb_cmd))) {
                if ((1U & (IData)(vlSelfRef.hb_cmd))) {
                    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__ridx = 0U;
                    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__acc = 0U;
                    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__rstate = 1U;
                } else {
                    if (vlSelfRef.d_mode) {
                        if (vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__decn) {
                            __Vdly__edges__BRA__1__KET____DOT__u_hebb__DOT__wh 
                                = (0xffffU & ((IData)(vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__wh) 
                                              - (IData)(1U)));
                            __Vdly__edges__BRA__1__KET____DOT__u_hebb__DOT__age = 0U;
                        } else {
                            __Vdly__edges__BRA__1__KET____DOT__u_hebb__DOT__age 
                                = (0xffffffU & ((IData)(1U) 
                                                + vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__age));
                        }
                    } else if (vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__hlend) {
                        vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__j = 6U;
                        __VdlyVal__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v2 
                            = vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__c
                            [6U];
                        __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v2 = 1U;
                        vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__j = 5U;
                        __Vdly__edges__BRA__1__KET____DOT__u_hebb__DOT__hl_cnt = 0U;
                        __VdlyVal__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v3 
                            = vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__c
                            [5U];
                        __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v3 = 1U;
                        vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__j = 4U;
                        __VdlyVal__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v4 
                            = vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__c
                            [4U];
                        __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v4 = 1U;
                        vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__j = 3U;
                        __VdlyVal__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v5 
                            = vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__c
                            [3U];
                        __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v5 = 1U;
                        vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__j = 2U;
                        __VdlyVal__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v6 
                            = vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__c
                            [2U];
                        __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v6 = 1U;
                        vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__j = 1U;
                        __VdlyVal__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v7 
                            = vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__c
                            [1U];
                        __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v7 = 1U;
                        vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__j = 0U;
                        __VdlyVal__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v8 
                            = vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__c
                            [0U];
                        __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v8 = 1U;
                    } else {
                        __Vdly__edges__BRA__1__KET____DOT__u_hebb__DOT__hl_cnt 
                            = (0xffffU & ((IData)(1U) 
                                          + (IData)(vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__hl_cnt)));
                    }
                    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__o_done = 1U;
                }
            } else if ((1U & (IData)(vlSelfRef.hb_cmd))) {
                if (vlSelfRef.d_mode) {
                    if ((0xffffU == (IData)(vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__wh))) {
                        vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__o_ovf = 1U;
                    } else {
                        __Vdly__edges__BRA__1__KET____DOT__u_hebb__DOT__wh 
                            = (0xffffU & ((IData)(1U) 
                                          + (IData)(vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__wh)));
                    }
                } else if ((0xffU == vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__c
                            [0U])) {
                    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__o_ovf = 1U;
                } else {
                    __VdlyVal__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v10 
                        = (0xffU & ((IData)(1U) + vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__c
                                    [0U]));
                    __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v10 = 1U;
                }
                vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__o_done = 1U;
            }
        }
        vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__o_done = 0U;
        if (vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__rstate) {
            if ((8U == (IData)(vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__ridx))) {
                vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__o_w 
                    = vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__wout;
                vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__o_done = 1U;
                vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__rstate = 0U;
            } else {
                vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__acc 
                    = (0x1ffffU & (vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__acc 
                                   + vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__addw));
                vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__ridx 
                    = (0x1fU & ((IData)(1U) + (IData)(vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__ridx)));
            }
        } else if ((4U & (IData)(vlSelfRef.u_core__DOT__hb_sel))) {
            if ((4U & (IData)(vlSelfRef.hb_cmd))) {
                if ((1U & (~ ((IData)(vlSelfRef.hb_cmd) 
                              >> 1U)))) {
                    if ((1U & (IData)(vlSelfRef.hb_cmd))) {
                        if (vlSelfRef.d_mode) {
                            if ((0xffffU == (IData)(vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__wh))) {
                                vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__o_ovf = 1U;
                            } else {
                                __Vdly__edges__BRA__2__KET____DOT__u_hebb__DOT__wh 
                                    = (0xffffU & ((IData)(1U) 
                                                  + (IData)(vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__wh)));
                            }
                        } else if ((8U <= (IData)(vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__gcl))) {
                            if ((0xffU == vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__c
                                 [7U])) {
                                vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__o_ovf = 1U;
                            } else {
                                __VdlyVal__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v0 
                                    = (0xffU & ((IData)(1U) 
                                                + vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__c
                                                [7U]));
                                __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v0 = 1U;
                            }
                        } else if ((0xffU == vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__c
                                    [(7U & (IData)(vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__gcl))])) {
                            vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__o_ovf = 1U;
                        } else {
                            __VdlyVal__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v1 
                                = (0xffU & ((IData)(1U) 
                                            + vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__c
                                            [(7U & (IData)(vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__gcl))]));
                            __VdlyDim0__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v1 
                                = (7U & (IData)(vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__gcl));
                            __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v1 = 1U;
                        }
                        vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__o_done = 1U;
                    } else {
                        vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__base 
                            = vlSelfRef.hb_base;
                        vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__o_done = 1U;
                    }
                }
            } else if ((2U & (IData)(vlSelfRef.hb_cmd))) {
                if ((1U & (IData)(vlSelfRef.hb_cmd))) {
                    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__ridx = 0U;
                    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__acc = 0U;
                    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__rstate = 1U;
                } else {
                    if (vlSelfRef.d_mode) {
                        if (vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__decn) {
                            __Vdly__edges__BRA__2__KET____DOT__u_hebb__DOT__wh 
                                = (0xffffU & ((IData)(vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__wh) 
                                              - (IData)(1U)));
                            __Vdly__edges__BRA__2__KET____DOT__u_hebb__DOT__age = 0U;
                        } else {
                            __Vdly__edges__BRA__2__KET____DOT__u_hebb__DOT__age 
                                = (0xffffffU & ((IData)(1U) 
                                                + vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__age));
                        }
                    } else if (vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__hlend) {
                        vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__j = 6U;
                        __VdlyVal__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v2 
                            = vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__c
                            [6U];
                        __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v2 = 1U;
                        vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__j = 5U;
                        __Vdly__edges__BRA__2__KET____DOT__u_hebb__DOT__hl_cnt = 0U;
                        __VdlyVal__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v3 
                            = vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__c
                            [5U];
                        __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v3 = 1U;
                        vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__j = 4U;
                        __VdlyVal__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v4 
                            = vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__c
                            [4U];
                        __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v4 = 1U;
                        vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__j = 3U;
                        __VdlyVal__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v5 
                            = vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__c
                            [3U];
                        __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v5 = 1U;
                        vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__j = 2U;
                        __VdlyVal__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v6 
                            = vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__c
                            [2U];
                        __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v6 = 1U;
                        vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__j = 1U;
                        __VdlyVal__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v7 
                            = vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__c
                            [1U];
                        __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v7 = 1U;
                        vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__j = 0U;
                        __VdlyVal__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v8 
                            = vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__c
                            [0U];
                        __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v8 = 1U;
                    } else {
                        __Vdly__edges__BRA__2__KET____DOT__u_hebb__DOT__hl_cnt 
                            = (0xffffU & ((IData)(1U) 
                                          + (IData)(vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__hl_cnt)));
                    }
                    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__o_done = 1U;
                }
            } else if ((1U & (IData)(vlSelfRef.hb_cmd))) {
                if (vlSelfRef.d_mode) {
                    if ((0xffffU == (IData)(vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__wh))) {
                        vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__o_ovf = 1U;
                    } else {
                        __Vdly__edges__BRA__2__KET____DOT__u_hebb__DOT__wh 
                            = (0xffffU & ((IData)(1U) 
                                          + (IData)(vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__wh)));
                    }
                } else if ((0xffU == vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__c
                            [0U])) {
                    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__o_ovf = 1U;
                } else {
                    __VdlyVal__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v10 
                        = (0xffU & ((IData)(1U) + vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__c
                                    [0U]));
                    __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v10 = 1U;
                }
                vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__o_done = 1U;
            }
        }
        vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__o_done = 0U;
        if (vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__rstate) {
            if ((8U == (IData)(vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__ridx))) {
                vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__o_w 
                    = vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__wout;
                vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__o_done = 1U;
                vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__rstate = 0U;
            } else {
                vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__acc 
                    = (0x1ffffU & (vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__acc 
                                   + vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__addw));
                vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__ridx 
                    = (0x1fU & ((IData)(1U) + (IData)(vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__ridx)));
            }
        } else if ((8U & (IData)(vlSelfRef.u_core__DOT__hb_sel))) {
            if ((4U & (IData)(vlSelfRef.hb_cmd))) {
                if ((1U & (~ ((IData)(vlSelfRef.hb_cmd) 
                              >> 1U)))) {
                    if ((1U & (IData)(vlSelfRef.hb_cmd))) {
                        if (vlSelfRef.d_mode) {
                            if ((0xffffU == (IData)(vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__wh))) {
                                vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__o_ovf = 1U;
                            } else {
                                __Vdly__edges__BRA__3__KET____DOT__u_hebb__DOT__wh 
                                    = (0xffffU & ((IData)(1U) 
                                                  + (IData)(vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__wh)));
                            }
                        } else if ((8U <= (IData)(vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__gcl))) {
                            if ((0xffU == vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__c
                                 [7U])) {
                                vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__o_ovf = 1U;
                            } else {
                                __VdlyVal__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v0 
                                    = (0xffU & ((IData)(1U) 
                                                + vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__c
                                                [7U]));
                                __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v0 = 1U;
                            }
                        } else if ((0xffU == vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__c
                                    [(7U & (IData)(vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__gcl))])) {
                            vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__o_ovf = 1U;
                        } else {
                            __VdlyVal__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v1 
                                = (0xffU & ((IData)(1U) 
                                            + vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__c
                                            [(7U & (IData)(vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__gcl))]));
                            __VdlyDim0__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v1 
                                = (7U & (IData)(vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__gcl));
                            __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v1 = 1U;
                        }
                        vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__o_done = 1U;
                    } else {
                        vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__base 
                            = vlSelfRef.hb_base;
                        vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__o_done = 1U;
                    }
                }
            } else if ((2U & (IData)(vlSelfRef.hb_cmd))) {
                if ((1U & (IData)(vlSelfRef.hb_cmd))) {
                    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__ridx = 0U;
                    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__acc = 0U;
                    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__rstate = 1U;
                } else {
                    if (vlSelfRef.d_mode) {
                        if (vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__decn) {
                            __Vdly__edges__BRA__3__KET____DOT__u_hebb__DOT__wh 
                                = (0xffffU & ((IData)(vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__wh) 
                                              - (IData)(1U)));
                            __Vdly__edges__BRA__3__KET____DOT__u_hebb__DOT__age = 0U;
                        } else {
                            __Vdly__edges__BRA__3__KET____DOT__u_hebb__DOT__age 
                                = (0xffffffU & ((IData)(1U) 
                                                + vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__age));
                        }
                    } else if (vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__hlend) {
                        vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__j = 6U;
                        __VdlyVal__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v2 
                            = vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__c
                            [6U];
                        __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v2 = 1U;
                        vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__j = 5U;
                        __Vdly__edges__BRA__3__KET____DOT__u_hebb__DOT__hl_cnt = 0U;
                        __VdlyVal__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v3 
                            = vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__c
                            [5U];
                        __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v3 = 1U;
                        vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__j = 4U;
                        __VdlyVal__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v4 
                            = vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__c
                            [4U];
                        __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v4 = 1U;
                        vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__j = 3U;
                        __VdlyVal__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v5 
                            = vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__c
                            [3U];
                        __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v5 = 1U;
                        vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__j = 2U;
                        __VdlyVal__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v6 
                            = vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__c
                            [2U];
                        __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v6 = 1U;
                        vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__j = 1U;
                        __VdlyVal__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v7 
                            = vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__c
                            [1U];
                        __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v7 = 1U;
                        vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__j = 0U;
                        __VdlyVal__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v8 
                            = vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__c
                            [0U];
                        __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v8 = 1U;
                    } else {
                        __Vdly__edges__BRA__3__KET____DOT__u_hebb__DOT__hl_cnt 
                            = (0xffffU & ((IData)(1U) 
                                          + (IData)(vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__hl_cnt)));
                    }
                    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__o_done = 1U;
                }
            } else if ((1U & (IData)(vlSelfRef.hb_cmd))) {
                if (vlSelfRef.d_mode) {
                    if ((0xffffU == (IData)(vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__wh))) {
                        vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__o_ovf = 1U;
                    } else {
                        __Vdly__edges__BRA__3__KET____DOT__u_hebb__DOT__wh 
                            = (0xffffU & ((IData)(1U) 
                                          + (IData)(vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__wh)));
                    }
                } else if ((0xffU == vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__c
                            [0U])) {
                    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__o_ovf = 1U;
                } else {
                    __VdlyVal__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v10 
                        = (0xffU & ((IData)(1U) + vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__c
                                    [0U]));
                    __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v10 = 1U;
                }
                vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__o_done = 1U;
            }
        }
        vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__o_done = 0U;
        if (vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__rstate) {
            if ((8U == (IData)(vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__ridx))) {
                vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__o_w 
                    = vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__wout;
                vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__o_done = 1U;
                vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__rstate = 0U;
            } else {
                vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__acc 
                    = (0x1ffffU & (vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__acc 
                                   + vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__addw));
                vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__ridx 
                    = (0x1fU & ((IData)(1U) + (IData)(vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__ridx)));
            }
        } else if ((1U & (IData)(vlSelfRef.u_core__DOT__hb_sel))) {
            if ((4U & (IData)(vlSelfRef.hb_cmd))) {
                if ((1U & (~ ((IData)(vlSelfRef.hb_cmd) 
                              >> 1U)))) {
                    if ((1U & (IData)(vlSelfRef.hb_cmd))) {
                        if (vlSelfRef.d_mode) {
                            if ((0xffffU == (IData)(vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__wh))) {
                                vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__o_ovf = 1U;
                            } else {
                                __Vdly__edges__BRA__0__KET____DOT__u_hebb__DOT__wh 
                                    = (0xffffU & ((IData)(1U) 
                                                  + (IData)(vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__wh)));
                            }
                        } else if ((8U <= (IData)(vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__gcl))) {
                            if ((0xffU == vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__c
                                 [7U])) {
                                vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__o_ovf = 1U;
                            } else {
                                __VdlyVal__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v0 
                                    = (0xffU & ((IData)(1U) 
                                                + vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__c
                                                [7U]));
                                __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v0 = 1U;
                            }
                        } else if ((0xffU == vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__c
                                    [(7U & (IData)(vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__gcl))])) {
                            vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__o_ovf = 1U;
                        } else {
                            __VdlyVal__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v1 
                                = (0xffU & ((IData)(1U) 
                                            + vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__c
                                            [(7U & (IData)(vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__gcl))]));
                            __VdlyDim0__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v1 
                                = (7U & (IData)(vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__gcl));
                            __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v1 = 1U;
                        }
                        vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__o_done = 1U;
                    } else {
                        vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__base 
                            = vlSelfRef.hb_base;
                        vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__o_done = 1U;
                    }
                }
            } else if ((2U & (IData)(vlSelfRef.hb_cmd))) {
                if ((1U & (IData)(vlSelfRef.hb_cmd))) {
                    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__ridx = 0U;
                    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__acc = 0U;
                    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__rstate = 1U;
                } else {
                    if (vlSelfRef.d_mode) {
                        if (vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__decn) {
                            __Vdly__edges__BRA__0__KET____DOT__u_hebb__DOT__wh 
                                = (0xffffU & ((IData)(vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__wh) 
                                              - (IData)(1U)));
                            __Vdly__edges__BRA__0__KET____DOT__u_hebb__DOT__age = 0U;
                        } else {
                            __Vdly__edges__BRA__0__KET____DOT__u_hebb__DOT__age 
                                = (0xffffffU & ((IData)(1U) 
                                                + vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__age));
                        }
                    } else if (vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__hlend) {
                        vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__j = 6U;
                        __VdlyVal__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v2 
                            = vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__c
                            [6U];
                        __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v2 = 1U;
                        vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__j = 5U;
                        __Vdly__edges__BRA__0__KET____DOT__u_hebb__DOT__hl_cnt = 0U;
                        __VdlyVal__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v3 
                            = vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__c
                            [5U];
                        __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v3 = 1U;
                        vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__j = 4U;
                        __VdlyVal__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v4 
                            = vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__c
                            [4U];
                        __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v4 = 1U;
                        vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__j = 3U;
                        __VdlyVal__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v5 
                            = vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__c
                            [3U];
                        __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v5 = 1U;
                        vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__j = 2U;
                        __VdlyVal__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v6 
                            = vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__c
                            [2U];
                        __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v6 = 1U;
                        vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__j = 1U;
                        __VdlyVal__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v7 
                            = vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__c
                            [1U];
                        __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v7 = 1U;
                        vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__j = 0U;
                        __VdlyVal__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v8 
                            = vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__c
                            [0U];
                        __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v8 = 1U;
                    } else {
                        __Vdly__edges__BRA__0__KET____DOT__u_hebb__DOT__hl_cnt 
                            = (0xffffU & ((IData)(1U) 
                                          + (IData)(vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__hl_cnt)));
                    }
                    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__o_done = 1U;
                }
            } else if ((1U & (IData)(vlSelfRef.hb_cmd))) {
                if (vlSelfRef.d_mode) {
                    if ((0xffffU == (IData)(vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__wh))) {
                        vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__o_ovf = 1U;
                    } else {
                        __Vdly__edges__BRA__0__KET____DOT__u_hebb__DOT__wh 
                            = (0xffffU & ((IData)(1U) 
                                          + (IData)(vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__wh)));
                    }
                } else if ((0xffU == vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__c
                            [0U])) {
                    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__o_ovf = 1U;
                } else {
                    __VdlyVal__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v10 
                        = (0xffU & ((IData)(1U) + vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__c
                                    [0U]));
                    __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v10 = 1U;
                }
                vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__o_done = 1U;
            }
        }
        vlSelfRef.u_core__DOT__df_wr = 0U;
        vlSelfRef.u_core__DOT__df_rd = 0U;
        vlSelfRef.u_core__DOT__hb_cmd = 0U;
        vlSelfRef.u_core__DOT__eg_fire = 0U;
        __Vdly__u_core__DOT__lo_valid = 0U;
        __Vdly__u_core__DOT__lx_valid = 0U;
        if ((0x10U & (IData)(vlSelfRef.u_core__DOT__state))) {
            if ((8U & (IData)(vlSelfRef.u_core__DOT__state))) {
                __Vdly__u_core__DOT__state = 2U;
            } else if ((4U & (IData)(vlSelfRef.u_core__DOT__state))) {
                if ((2U & (IData)(vlSelfRef.u_core__DOT__state))) {
                    __Vdly__u_core__DOT__state = 2U;
                } else if ((1U & (IData)(vlSelfRef.u_core__DOT__state))) {
                    vlSelfRef.u_core__DOT__eff_p = vlSelfRef.u_core__DOT__prod_p;
                    __Vdly__u_core__DOT__state = 0x13U;
                } else if (vlSelfRef.hb_done) {
                    vlSelfRef.u_core__DOT__eff_w = vlSelfRef.u_core__DOT__hb_wq;
                    __Vdly__u_core__DOT__state = 0x15U;
                }
            } else if ((2U & (IData)(vlSelfRef.u_core__DOT__state))) {
                if ((1U & (IData)(vlSelfRef.u_core__DOT__state))) {
                    __Vfunc_u_core__DOT__sclip16__28__v 
                        = (0xfffffffffULL & (vlSelfRef.u_core__DOT__act_e 
                                             + VL_SHIFTRS_QQI(36,36,32, vlSelfRef.u_core__DOT__eff_pe, 0xfU)));
                    __Vfunc_u_core__DOT__sclip16__28__Vfuncout 
                        = (VL_LTS_IQQ(36, 0x7fffULL, __Vfunc_u_core__DOT__sclip16__28__v)
                            ? 0x7fffU : (VL_GTS_IQQ(36, 0xfffff8000ULL, __Vfunc_u_core__DOT__sclip16__28__v)
                                          ? 0x8000U
                                          : (0xffffU 
                                             & (IData)(__Vfunc_u_core__DOT__sclip16__28__v))));
                    __Vdly__u_core__DOT__act = __Vfunc_u_core__DOT__sclip16__28__Vfuncout;
                    __Vdly__u_core__DOT__ci_ready = 
                        (1U & (~ ((IData)(vlSelfRef.s_tick) 
                                  | (IData)(vlSelfRef.u_core__DOT__tick_pend))));
                    __Vdly__u_core__DOT__state = 2U;
                } else if ((4U == (IData)(vlSelfRef.u_core__DOT__eidx))) {
                    __Vdly__u_core__DOT__act = 0U;
                    __Vdly__u_core__DOT__refr = vlSelfRef.d_refr;
                    __Vdly__u_core__DOT__ci_ready = 
                        (1U & (~ ((IData)(vlSelfRef.s_tick) 
                                  | (IData)(vlSelfRef.u_core__DOT__tick_pend))));
                    __Vdly__u_core__DOT__state = 2U;
                } else if (vlSelfRef.u_core__DOT__ev
                           [(3U & (IData)(vlSelfRef.u_core__DOT__eidx))]) {
                    __Vdly__u_core__DOT__lx_valid = 1U;
                    vlSelfRef.u_core__DOT__lx_op = 2U;
                    vlSelfRef.u_core__DOT__lx_dst = 
                        vlSelfRef.u_core__DOT__etab
                        [(3U & (IData)(vlSelfRef.u_core__DOT__eidx))];
                    vlSelfRef.u_core__DOT__lx_src = vlSelfRef.u_core__DOT__cell_id;
                    vlSelfRef.u_core__DOT__lx_dat = vlSelfRef.u_core__DOT__afire;
                    vlSelfRef.u_core__DOT__lx_a0 = 0U;
                    vlSelfRef.u_core__DOT__lx_a1 = 0U;
                    vlSelfRef.u_core__DOT__lx_a2 = 0U;
                    if (((IData)(vlSelfRef.u_core__DOT__lx_valid) 
                         & (IData)(vlSelfRef.lx_grant))) {
                        __Vdly__u_core__DOT__eidx = 
                            (7U & ((IData)(1U) + (IData)(vlSelfRef.u_core__DOT__eidx)));
                        __Vdly__u_core__DOT__lx_valid = 0U;
                    }
                } else {
                    __Vdly__u_core__DOT__eidx = (7U 
                                                 & ((IData)(1U) 
                                                    + (IData)(vlSelfRef.u_core__DOT__eidx)));
                }
            } else if ((1U & (IData)(vlSelfRef.u_core__DOT__state))) {
                __Vfunc_u_core__DOT__sclip16__29__v 
                    = vlSelfRef.u_core__DOT__leak_sum;
                __Vfunc_u_core__DOT__sclip16__29__Vfuncout 
                    = (VL_LTS_IQQ(36, 0x7fffULL, __Vfunc_u_core__DOT__sclip16__29__v)
                        ? 0x7fffU : (VL_GTS_IQQ(36, 0xfffff8000ULL, __Vfunc_u_core__DOT__sclip16__29__v)
                                      ? 0x8000U : (0xffffU 
                                                   & (IData)(__Vfunc_u_core__DOT__sclip16__29__v))));
                if ((VL_GTES_III(16, (IData)(vlSelfRef.u_core__DOT__act), (IData)(vlSelfRef.d_thresh)) 
                     & (0U == (IData)(vlSelfRef.u_core__DOT__refr)))) {
                    __Vdly__u_core__DOT__eidx = 0U;
                    vlSelfRef.u_core__DOT__afire = vlSelfRef.u_core__DOT__act;
                    vlSelfRef.u_core__DOT__eg_fire = 1U;
                    __Vdly__u_core__DOT__state = 0x12U;
                } else {
                    if ((0U != (IData)(vlSelfRef.u_core__DOT__refr))) {
                        __Vdly__u_core__DOT__refr = 
                            (0xffffU & ((IData)(vlSelfRef.u_core__DOT__refr) 
                                        - (IData)(1U)));
                    }
                    __Vdly__u_core__DOT__ci_ready = 
                        (1U & (~ ((IData)(vlSelfRef.s_tick) 
                                  | (IData)(vlSelfRef.u_core__DOT__tick_pend))));
                    __Vdly__u_core__DOT__state = 2U;
                }
                __Vdly__u_core__DOT__act = __Vfunc_u_core__DOT__sclip16__29__Vfuncout;
            } else if (vlSelfRef.hb_done) {
                __Vdly__u_core__DOT__eidx = (7U & ((IData)(1U) 
                                                   + (IData)(vlSelfRef.u_core__DOT__eidx)));
                __Vdly__u_core__DOT__state = 0xfU;
            }
        } else if ((8U & (IData)(vlSelfRef.u_core__DOT__state))) {
            if ((4U & (IData)(vlSelfRef.u_core__DOT__state))) {
                if ((2U & (IData)(vlSelfRef.u_core__DOT__state))) {
                    if ((1U & (IData)(vlSelfRef.u_core__DOT__state))) {
                        if ((4U == (IData)(vlSelfRef.u_core__DOT__eidx))) {
                            __Vdly__u_core__DOT__state = 0x11U;
                        } else if (vlSelfRef.u_core__DOT__ev
                                   [(3U & (IData)(vlSelfRef.u_core__DOT__eidx))]) {
                            vlSelfRef.u_core__DOT__hb_sel 
                                = (0xfU & ((IData)(1U) 
                                           << (3U & (IData)(vlSelfRef.u_core__DOT__eidx))));
                            vlSelfRef.u_core__DOT__hb_cmd = 2U;
                            __Vdly__u_core__DOT__state = 0x10U;
                        } else {
                            __Vdly__u_core__DOT__eidx 
                                = (7U & ((IData)(1U) 
                                         + (IData)(vlSelfRef.u_core__DOT__eidx)));
                        }
                    } else {
                        __Vdly__u_core__DOT__eidx = 0U;
                        __Vdly__u_core__DOT__state = 0xfU;
                    }
                } else if ((1U & (IData)(vlSelfRef.u_core__DOT__state))) {
                    __Vdly__u_core__DOT__lo_valid = 1U;
                    vlSelfRef.u_core__DOT__lo_op = 
                        ((IData)(vlSelfRef.u_core__DOT__resp_nak)
                          ? 6U : 5U);
                    vlSelfRef.u_core__DOT__lo_dst = vlSelfRef.u_core__DOT__lr_src;
                    vlSelfRef.u_core__DOT__lo_src = vlSelfRef.u_core__DOT__cell_id;
                    vlSelfRef.u_core__DOT__lo_a0 = 0U;
                    vlSelfRef.u_core__DOT__lo_a1 = 0U;
                    vlSelfRef.u_core__DOT__lo_a2 = vlSelfRef.u_core__DOT__lr_a2;
                    vlSelfRef.u_core__DOT__lo_dat = vlSelfRef.u_core__DOT__viewdat;
                    if (((IData)(vlSelfRef.u_core__DOT__lo_valid) 
                         & (IData)(vlSelfRef.lo_grant))) {
                        __Vdly__u_core__DOT__lo_valid = 0U;
                        __Vdly__u_core__DOT__ci_ready 
                            = (1U & (~ ((IData)(vlSelfRef.s_tick) 
                                        | (IData)(vlSelfRef.u_core__DOT__tick_pend))));
                        __Vdly__u_core__DOT__state = 2U;
                    }
                } else if (vlSelfRef.df_rstb) {
                    vlSelfRef.u_core__DOT__viewdat 
                        = vlSelfRef.df_rdata;
                    vlSelfRef.u_core__DOT__resp_nak = 0U;
                    __Vdly__u_core__DOT__state = 0xdU;
                }
            } else if ((2U & (IData)(vlSelfRef.u_core__DOT__state))) {
                if ((1U & (IData)(vlSelfRef.u_core__DOT__state))) {
                    if (vlSelfRef.hb_done) {
                        __Vdly__u_core__DOT__wacc = 
                            (0x7ffffU & ((vlSelfRef.u_core__DOT__wacc 
                                          + (IData)(vlSelfRef.hb_w)) 
                                         + (IData)(vlSelfRef.u_core__DOT__rq_credit)));
                        __Vdly__u_core__DOT__eidx = 
                            (7U & ((IData)(1U) + (IData)(vlSelfRef.u_core__DOT__eidx)));
                        __Vdly__u_core__DOT__state = 0xaU;
                    }
                } else if ((4U == (IData)(vlSelfRef.u_core__DOT__eidx))) {
                    vlSelfRef.u_core__DOT__viewdat 
                        = ((0U != (7U & (vlSelfRef.u_core__DOT__wacc 
                                         >> 0x10U)))
                            ? 0xffffU : (0xffffU & vlSelfRef.u_core__DOT__wacc));
                    vlSelfRef.u_core__DOT__resp_nak = 0U;
                    __Vdly__u_core__DOT__state = 0xdU;
                } else if (vlSelfRef.u_core__DOT__ev
                           [(3U & (IData)(vlSelfRef.u_core__DOT__eidx))]) {
                    vlSelfRef.u_core__DOT__hb_sel = 
                        (0xfU & ((IData)(1U) << (3U 
                                                 & (IData)(vlSelfRef.u_core__DOT__eidx))));
                    vlSelfRef.u_core__DOT__hb_cmd = 3U;
                    __Vdly__u_core__DOT__state = 0xbU;
                } else {
                    __Vdly__u_core__DOT__eidx = (7U 
                                                 & ((IData)(1U) 
                                                    + (IData)(vlSelfRef.u_core__DOT__eidx)));
                }
            } else if ((1U & (IData)(vlSelfRef.u_core__DOT__state))) {
                if (vlSelfRef.u_core__DOT__bound) {
                    if ((0U == (3U & (IData)(vlSelfRef.u_core__DOT__lr_a0)))) {
                        vlSelfRef.u_core__DOT__viewdat 
                            = vlSelfRef.u_core__DOT__act;
                        vlSelfRef.u_core__DOT__resp_nak = 0U;
                        __Vdly__u_core__DOT__state = 0xdU;
                    } else if ((1U == (3U & (IData)(vlSelfRef.u_core__DOT__lr_a0)))) {
                        __Vdly__u_core__DOT__wacc = 0U;
                        __Vdly__u_core__DOT__eidx = 0U;
                        __Vdly__u_core__DOT__state = 0xaU;
                    } else if ((2U == (3U & (IData)(vlSelfRef.u_core__DOT__lr_a0)))) {
                        vlSelfRef.u_core__DOT__df_rd = 1U;
                        vlSelfRef.u_core__DOT__df_addr 
                            = (0xfU & (IData)(vlSelfRef.u_core__DOT__lr_a1));
                        __Vdly__u_core__DOT__state = 0xcU;
                    } else {
                        vlSelfRef.u_core__DOT__resp_nak = 1U;
                        vlSelfRef.u_core__DOT__viewdat = 0U;
                        __Vdly__u_core__DOT__state = 0xdU;
                    }
                } else {
                    vlSelfRef.u_core__DOT__resp_nak = 1U;
                    vlSelfRef.u_core__DOT__viewdat = 0U;
                    __Vdly__u_core__DOT__state = 0xdU;
                }
            } else if (vlSelfRef.hb_done) {
                vlSelfRef.u_core__DOT__hb_cmd = 3U;
                __Vdly__u_core__DOT__state = 0x14U;
            }
        } else if ((4U & (IData)(vlSelfRef.u_core__DOT__state))) {
            if ((2U & (IData)(vlSelfRef.u_core__DOT__state))) {
                if ((1U & (IData)(vlSelfRef.u_core__DOT__state))) {
                    if ((4U == (IData)(vlSelfRef.u_core__DOT__eidx))) {
                        __Vdly__u_core__DOT__ci_ready 
                            = (1U & (~ ((IData)(vlSelfRef.s_tick) 
                                        | (IData)(vlSelfRef.u_core__DOT__tick_pend))));
                        __Vdly__u_core__DOT__state = 2U;
                    } else if ((vlSelfRef.u_core__DOT__ev
                                [(3U & (IData)(vlSelfRef.u_core__DOT__eidx))] 
                                & (vlSelfRef.u_core__DOT__etab
                                   [(3U & (IData)(vlSelfRef.u_core__DOT__eidx))] 
                                   == (IData)(vlSelfRef.u_core__DOT__lr_src)))) {
                        vlSelfRef.u_core__DOT__hb_sel 
                            = (0xfU & ((IData)(1U) 
                                       << (3U & (IData)(vlSelfRef.u_core__DOT__eidx))));
                        if (vlSelfRef.u_core__DOT__eg_live) {
                            vlSelfRef.u_core__DOT__hb_cmd = 5U;
                            vlSelfRef.u_core__DOT__hb_gcl 
                                = vlSelfRef.u_core__DOT__eg_gclass;
                            __Vdly__u_core__DOT__state = 8U;
                        } else {
                            vlSelfRef.u_core__DOT__hb_cmd = 3U;
                            __Vdly__u_core__DOT__state = 0x14U;
                        }
                    } else {
                        __Vdly__u_core__DOT__eidx = 
                            (7U & ((IData)(1U) + (IData)(vlSelfRef.u_core__DOT__eidx)));
                    }
                } else {
                    __Vdly__u_core__DOT__eidx = 0U;
                    __Vdly__u_core__DOT__state = 7U;
                }
            } else if ((1U & (IData)(vlSelfRef.u_core__DOT__state))) {
                if (vlSelfRef.hb_done) {
                    vlSelfRef.u_core__DOT__resp_nak = 0U;
                    vlSelfRef.u_core__DOT__viewdat = 0U;
                    __Vdly__u_core__DOT__state = 0xdU;
                }
            } else {
                __VdlyVal__u_core__DOT__etab__v0 = vlSelfRef.u_core__DOT__lr_src;
                __VdlyDim0__u_core__DOT__etab__v0 = 
                    (3U & (IData)(vlSelfRef.u_core__DOT__lr_a0));
                __VdlySet__u_core__DOT__etab__v0 = 1U;
                __VdlyDim0__u_core__DOT__ev__v0 = (3U 
                                                   & (IData)(vlSelfRef.u_core__DOT__lr_a0));
                vlSelfRef.u_core__DOT__hb_sel = (0xfU 
                                                 & ((IData)(1U) 
                                                    << 
                                                    (3U 
                                                     & (IData)(vlSelfRef.u_core__DOT__lr_a0))));
                vlSelfRef.u_core__DOT__hb_cmd = 4U;
                vlSelfRef.u_core__DOT__hb_base = vlSelfRef.u_core__DOT__lr_a1;
                __Vdly__u_core__DOT__state = 5U;
            }
        } else if ((2U & (IData)(vlSelfRef.u_core__DOT__state))) {
            if ((1U & (IData)(vlSelfRef.u_core__DOT__state))) {
                vlSelfRef.u_core__DOT__df_wr = 1U;
                vlSelfRef.u_core__DOT__df_addr = vlSelfRef.u_core__DOT__lr_a0;
                vlSelfRef.u_core__DOT__df_wdata = vlSelfRef.u_core__DOT__lr_a1;
                vlSelfRef.u_core__DOT__resp_nak = 0U;
                vlSelfRef.u_core__DOT__viewdat = 0U;
                __Vdly__u_core__DOT__state = 0xdU;
            } else if (vlSelfRef.u_core__DOT__tick_pend) {
                __Vdly__u_core__DOT__ci_ready = 0U;
                vlSelfRef.u_core__DOT__hb_sel = 0U;
                __Vdly__u_core__DOT__state = 0xeU;
            } else {
                __Vdly__u_core__DOT__ci_ready = (1U 
                                                 & (~ 
                                                    ((IData)(vlSelfRef.s_tick) 
                                                     | (IData)(vlSelfRef.u_core__DOT__tick_pend))));
                vlSelfRef.u_core__DOT__hb_sel = 0U;
                if (((IData)(vlSelfRef.ci_valid) & (IData)(vlSelfRef.u_core__DOT__ci_ready))) {
                    vlSelfRef.u_core__DOT__lr_src = vlSelfRef.ci_src;
                    vlSelfRef.u_core__DOT__lr_a0 = 
                        (0xfU & (IData)(vlSelfRef.ci_a0));
                    vlSelfRef.u_core__DOT__lr_a1 = vlSelfRef.ci_a1;
                    vlSelfRef.u_core__DOT__lr_a2 = vlSelfRef.ci_a2;
                    vlSelfRef.u_core__DOT__lr_dat = vlSelfRef.ci_dat;
                    __Vdly__u_core__DOT__ci_ready = 0U;
                    if ((4U & (IData)(vlSelfRef.ci_op))) {
                        if ((2U & (IData)(vlSelfRef.ci_op))) {
                            if ((1U & (IData)(vlSelfRef.ci_op))) {
                                vlSelfRef.u_core__DOT__resp_nak = 1U;
                                vlSelfRef.u_core__DOT__viewdat = 0U;
                                __Vdly__u_core__DOT__state = 0xdU;
                            } else {
                                __Vdly__u_core__DOT__state = 2U;
                            }
                        } else {
                            __Vdly__u_core__DOT__state = 2U;
                        }
                    } else {
                        __Vdly__u_core__DOT__state 
                            = ((2U & (IData)(vlSelfRef.ci_op))
                                ? ((1U & (IData)(vlSelfRef.ci_op))
                                    ? 9U : 6U) : ((1U 
                                                   & (IData)(vlSelfRef.ci_op))
                                                   ? 4U
                                                   : 3U));
                    }
                }
            }
        } else if ((1U & (IData)(vlSelfRef.u_core__DOT__state))) {
            __Vdly__u_core__DOT__ci_ready = 1U;
            if (((IData)(vlSelfRef.ci_valid) & (IData)(vlSelfRef.u_core__DOT__ci_ready))) {
                __Vdly__u_core__DOT__ci_ready = 0U;
                vlSelfRef.u_core__DOT__lr_src = vlSelfRef.ci_src;
                vlSelfRef.u_core__DOT__lr_a2 = vlSelfRef.ci_a2;
                if ((0U == (IData)(vlSelfRef.ci_op))) {
                    vlSelfRef.u_core__DOT__cell_id 
                        = (0xfU & (IData)(vlSelfRef.ci_a0));
                    vlSelfRef.u_core__DOT__bound = 1U;
                    vlSelfRef.u_core__DOT__resp_nak = 0U;
                } else {
                    vlSelfRef.u_core__DOT__resp_nak = 1U;
                }
                vlSelfRef.u_core__DOT__viewdat = 0U;
                __Vdly__u_core__DOT__state = 0xdU;
            }
        } else {
            __Vdly__u_core__DOT__state = 1U;
        }
    } else {
        __Vdly__u_core__DOT__tick_pend = 0U;
        __VdlySet__u_core__DOT__u_rq__DOT__R__v2 = 1U;
        __Vdly__u_egbuf__DOT__a_v = 0U;
        vlSelfRef.u_egbuf__DOT__b_v = 0U;
        vlSelfRef.u_egbuf__DOT__a_q[0U] = 0U;
        vlSelfRef.u_egbuf__DOT__a_q[1U] = 0U;
        vlSelfRef.u_egbuf__DOT__a_q[2U] = 0U;
        vlSelfRef.u_egbuf__DOT__b_q[0U] = 0U;
        vlSelfRef.u_egbuf__DOT__b_q[1U] = 0U;
        vlSelfRef.u_egbuf__DOT__b_q[2U] = 0U;
        __Vdly__u_inbuf__DOT__a_v = 0U;
        vlSelfRef.u_inbuf__DOT__b_v = 0U;
        vlSelfRef.u_inbuf__DOT__a_q[0U] = 0U;
        vlSelfRef.u_inbuf__DOT__a_q[1U] = 0U;
        vlSelfRef.u_inbuf__DOT__a_q[2U] = 0U;
        vlSelfRef.u_inbuf__DOT__b_q[0U] = 0U;
        vlSelfRef.u_inbuf__DOT__b_q[1U] = 0U;
        vlSelfRef.u_inbuf__DOT__b_q[2U] = 0U;
        vlSelfRef.u_core__DOT__u_eg__DOT__f = 0U;
        vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__j = 1U;
        vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__ridx = 0U;
        vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__acc = 0U;
        vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__o_done = 0U;
        vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__o_w = 0U;
        vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__o_ovf = 0U;
        __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v11 = 1U;
        vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__j = 2U;
        __Vdly__edges__BRA__1__KET____DOT__u_hebb__DOT__hl_cnt = 0U;
        __Vdly__edges__BRA__1__KET____DOT__u_hebb__DOT__wh = 0U;
        __Vdly__edges__BRA__1__KET____DOT__u_hebb__DOT__age = 0U;
        vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__base = 0U;
        vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__rstate = 0U;
        __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v12 = 1U;
        vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__j = 3U;
        __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v13 = 1U;
        vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__j = 4U;
        __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v14 = 1U;
        vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__j = 5U;
        __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v15 = 1U;
        vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__j = 6U;
        __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v16 = 1U;
        vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__j = 7U;
        __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v17 = 1U;
        vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__j = 8U;
        __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v18 = 1U;
        vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__j = 1U;
        vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__ridx = 0U;
        vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__acc = 0U;
        vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__o_done = 0U;
        vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__o_w = 0U;
        vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__o_ovf = 0U;
        __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v11 = 1U;
        vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__j = 2U;
        __Vdly__edges__BRA__2__KET____DOT__u_hebb__DOT__hl_cnt = 0U;
        __Vdly__edges__BRA__2__KET____DOT__u_hebb__DOT__wh = 0U;
        __Vdly__edges__BRA__2__KET____DOT__u_hebb__DOT__age = 0U;
        vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__base = 0U;
        vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__rstate = 0U;
        __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v12 = 1U;
        vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__j = 3U;
        __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v13 = 1U;
        vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__j = 4U;
        __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v14 = 1U;
        vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__j = 5U;
        __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v15 = 1U;
        vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__j = 6U;
        __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v16 = 1U;
        vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__j = 7U;
        __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v17 = 1U;
        vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__j = 8U;
        __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v18 = 1U;
        vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__j = 1U;
        vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__ridx = 0U;
        vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__acc = 0U;
        vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__o_done = 0U;
        vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__o_w = 0U;
        vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__o_ovf = 0U;
        __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v11 = 1U;
        vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__j = 2U;
        __Vdly__edges__BRA__3__KET____DOT__u_hebb__DOT__hl_cnt = 0U;
        __Vdly__edges__BRA__3__KET____DOT__u_hebb__DOT__wh = 0U;
        __Vdly__edges__BRA__3__KET____DOT__u_hebb__DOT__age = 0U;
        vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__base = 0U;
        vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__rstate = 0U;
        __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v12 = 1U;
        vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__j = 3U;
        __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v13 = 1U;
        vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__j = 4U;
        __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v14 = 1U;
        vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__j = 5U;
        __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v15 = 1U;
        vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__j = 6U;
        __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v16 = 1U;
        vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__j = 7U;
        __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v17 = 1U;
        vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__j = 8U;
        __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v18 = 1U;
        vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__j = 1U;
        vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__ridx = 0U;
        vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__acc = 0U;
        vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__o_done = 0U;
        vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__o_w = 0U;
        vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__o_ovf = 0U;
        __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v11 = 1U;
        vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__j = 2U;
        __Vdly__edges__BRA__0__KET____DOT__u_hebb__DOT__hl_cnt = 0U;
        __Vdly__edges__BRA__0__KET____DOT__u_hebb__DOT__wh = 0U;
        __Vdly__edges__BRA__0__KET____DOT__u_hebb__DOT__age = 0U;
        vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__base = 0U;
        vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__rstate = 0U;
        __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v12 = 1U;
        vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__j = 3U;
        __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v13 = 1U;
        vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__j = 4U;
        __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v14 = 1U;
        vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__j = 5U;
        __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v15 = 1U;
        vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__j = 6U;
        __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v16 = 1U;
        vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__j = 7U;
        __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v17 = 1U;
        vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__j = 8U;
        __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v18 = 1U;
        __Vdly__u_core__DOT__ci_ready = 0U;
        __Vdly__u_core__DOT__lo_valid = 0U;
        __Vdly__u_core__DOT__lx_valid = 0U;
        __Vdly__u_core__DOT__eidx = 0U;
        __Vdly__u_core__DOT__wacc = 0U;
        __Vdly__u_core__DOT__state = 0U;
        vlSelfRef.u_core__DOT__lo_op = 0U;
        vlSelfRef.u_core__DOT__lo_dst = 0U;
        vlSelfRef.u_core__DOT__lo_src = 0U;
        vlSelfRef.u_core__DOT__lo_a0 = 0U;
        vlSelfRef.u_core__DOT__lo_a1 = 0U;
        vlSelfRef.u_core__DOT__lo_a2 = 0U;
        vlSelfRef.u_core__DOT__lo_dat = 0U;
        vlSelfRef.u_core__DOT__lx_op = 0U;
        vlSelfRef.u_core__DOT__lx_dst = 0U;
        vlSelfRef.u_core__DOT__lx_src = 0U;
        vlSelfRef.u_core__DOT__lx_a0 = 0U;
        vlSelfRef.u_core__DOT__lx_a1 = 0U;
        vlSelfRef.u_core__DOT__lx_a2 = 0U;
        vlSelfRef.u_core__DOT__lx_dat = 0U;
        vlSelfRef.u_core__DOT__hb_cmd = 0U;
        vlSelfRef.u_core__DOT__hb_sel = 0U;
        vlSelfRef.u_core__DOT__hb_base = 0U;
        vlSelfRef.u_core__DOT__hb_gcl = 0U;
        vlSelfRef.u_core__DOT__eg_fire = 0U;
        vlSelfRef.u_core__DOT__df_wr = 0U;
        vlSelfRef.u_core__DOT__df_addr = 0U;
        vlSelfRef.u_core__DOT__df_wdata = 0U;
        vlSelfRef.u_core__DOT__df_rd = 0U;
        vlSelfRef.u_core__DOT__bound = 0U;
        vlSelfRef.u_core__DOT__cell_id = 0U;
        __Vdly__u_core__DOT__act = 0U;
        __Vdly__u_core__DOT__refr = 0U;
        vlSelfRef.u_core__DOT__viewdat = 0U;
        vlSelfRef.u_core__DOT__resp_nak = 0U;
        vlSelfRef.u_core__DOT__afire = 0U;
        vlSelfRef.u_core__DOT__lr_src = 0U;
        vlSelfRef.u_core__DOT__lr_a0 = 0U;
        vlSelfRef.u_core__DOT__lr_a1 = 0U;
        vlSelfRef.u_core__DOT__lr_a2 = 0U;
        vlSelfRef.u_core__DOT__lr_dat = 0U;
        vlSelfRef.u_core__DOT__eff_w = 0U;
        vlSelfRef.u_core__DOT__eff_p = 0ULL;
        __VdlySet__u_core__DOT__etab__v1 = 1U;
    }
    if (vlSelfRef.i_por_n) {
        if (((IData)(vlSelfRef.df_wr_g) & (0xdU != (IData)(vlSelfRef.df_addr_g)))) {
            __VdlyVal__u_df__DOT__dial__v0 = vlSelfRef.df_wdata_g;
            __VdlyDim0__u_df__DOT__dial__v0 = vlSelfRef.df_addr_g;
            __VdlySet__u_df__DOT__dial__v0 = 1U;
        }
        if (vlSelfRef.df_rd) {
            vlSelfRef.u_df__DOT__o_rdata = ((0xdU == (IData)(vlSelfRef.df_addr_g))
                                             ? (IData)(vlSelfRef.w_ftrace)
                                             : vlSelfRef.u_df__DOT__dial
                                            [vlSelfRef.df_addr_g]);
        }
    } else {
        __VdlySet__u_df__DOT__dial__v1 = 1U;
        vlSelfRef.u_df__DOT__o_rdata = 0U;
    }
    vlSelfRef.u_df__DOT__o_rstb = ((IData)(vlSelfRef.i_por_n) 
                                   && (IData)(vlSelfRef.df_rd));
    if (__VdlySet__u_core__DOT__u_rq__DOT__R__v0) {
        vlSelfRef.u_core__DOT__u_rq__DOT__R[__VdlyDim0__u_core__DOT__u_rq__DOT__R__v0] 
            = __VdlyVal__u_core__DOT__u_rq__DOT__R__v0;
    }
    if (__VdlySet__u_core__DOT__u_rq__DOT__R__v1) {
        vlSelfRef.u_core__DOT__u_rq__DOT__R[__VdlyDim0__u_core__DOT__u_rq__DOT__R__v1] 
            = __VdlyVal__u_core__DOT__u_rq__DOT__R__v1;
    }
    if (__VdlySet__u_core__DOT__u_rq__DOT__R__v2) {
        vlSelfRef.u_core__DOT__u_rq__DOT__R[0U] = 0U;
        vlSelfRef.u_core__DOT__u_rq__DOT__R[1U] = 0U;
        vlSelfRef.u_core__DOT__u_rq__DOT__R[2U] = 0U;
        vlSelfRef.u_core__DOT__u_rq__DOT__R[3U] = 0U;
    }
    if (__VdlySet__u_df__DOT__dial__v0) {
        vlSelfRef.u_df__DOT__dial[__VdlyDim0__u_df__DOT__dial__v0] 
            = __VdlyVal__u_df__DOT__dial__v0;
    }
    if (__VdlySet__u_df__DOT__dial__v1) {
        vlSelfRef.u_df__DOT__dial[0U] = 0x800U;
        vlSelfRef.u_df__DOT__dial[1U] = 0x80U;
        vlSelfRef.u_df__DOT__dial[2U] = 6U;
        vlSelfRef.u_df__DOT__dial[3U] = 0xcU;
        vlSelfRef.u_df__DOT__dial[4U] = 5U;
        vlSelfRef.u_df__DOT__dial[5U] = 0x6000U;
        vlSelfRef.u_df__DOT__dial[6U] = 4U;
        vlSelfRef.u_df__DOT__dial[7U] = 0x2ccdU;
        vlSelfRef.u_df__DOT__dial[8U] = 0x14U;
        vlSelfRef.u_df__DOT__dial[9U] = 0U;
        vlSelfRef.u_df__DOT__dial[0xaU] = 0x40U;
        vlSelfRef.u_df__DOT__dial[0xbU] = 2U;
        vlSelfRef.u_df__DOT__dial[0xcU] = 0U;
        vlSelfRef.u_df__DOT__dial[0xdU] = 0U;
        vlSelfRef.u_df__DOT__dial[0xeU] = 8U;
        vlSelfRef.u_df__DOT__dial[0xfU] = 8U;
    }
    vlSelfRef.u_egbuf__DOT__a_v = __Vdly__u_egbuf__DOT__a_v;
    vlSelfRef.u_inbuf__DOT__a_v = __Vdly__u_inbuf__DOT__a_v;
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__hl_cnt 
        = __Vdly__edges__BRA__1__KET____DOT__u_hebb__DOT__hl_cnt;
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__age 
        = __Vdly__edges__BRA__1__KET____DOT__u_hebb__DOT__age;
    if (__VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v0) {
        vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__c[7U] 
            = __VdlyVal__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v0;
    }
    if (__VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v1) {
        vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__c[__VdlyDim0__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v1] 
            = __VdlyVal__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v1;
    }
    if (__VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v2) {
        vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__c[7U] 
            = __VdlyVal__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v2;
    }
    if (__VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v3) {
        vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__c[6U] 
            = __VdlyVal__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v3;
    }
    if (__VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v4) {
        vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__c[5U] 
            = __VdlyVal__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v4;
    }
    if (__VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v5) {
        vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__c[4U] 
            = __VdlyVal__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v5;
    }
    if (__VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v6) {
        vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__c[3U] 
            = __VdlyVal__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v6;
    }
    if (__VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v7) {
        vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__c[2U] 
            = __VdlyVal__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v7;
    }
    if (__VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v8) {
        vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__c[1U] 
            = __VdlyVal__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v8;
        vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__c[0U] = 0U;
    }
    if (__VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v10) {
        vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__c[0U] 
            = __VdlyVal__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v10;
    }
    if (__VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v11) {
        vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__c[0U] = 0U;
    }
    if (__VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v12) {
        vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__c[1U] = 0U;
    }
    if (__VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v13) {
        vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__c[2U] = 0U;
    }
    if (__VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v14) {
        vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__c[3U] = 0U;
    }
    if (__VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v15) {
        vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__c[4U] = 0U;
    }
    if (__VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v16) {
        vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__c[5U] = 0U;
    }
    if (__VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v17) {
        vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__c[6U] = 0U;
    }
    if (__VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v18) {
        vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__c[7U] = 0U;
    }
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__wh 
        = __Vdly__edges__BRA__1__KET____DOT__u_hebb__DOT__wh;
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__hl_cnt 
        = __Vdly__edges__BRA__2__KET____DOT__u_hebb__DOT__hl_cnt;
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__age 
        = __Vdly__edges__BRA__2__KET____DOT__u_hebb__DOT__age;
    if (__VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v0) {
        vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__c[7U] 
            = __VdlyVal__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v0;
    }
    if (__VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v1) {
        vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__c[__VdlyDim0__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v1] 
            = __VdlyVal__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v1;
    }
    if (__VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v2) {
        vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__c[7U] 
            = __VdlyVal__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v2;
    }
    if (__VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v3) {
        vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__c[6U] 
            = __VdlyVal__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v3;
    }
    if (__VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v4) {
        vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__c[5U] 
            = __VdlyVal__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v4;
    }
    if (__VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v5) {
        vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__c[4U] 
            = __VdlyVal__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v5;
    }
    if (__VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v6) {
        vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__c[3U] 
            = __VdlyVal__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v6;
    }
    if (__VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v7) {
        vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__c[2U] 
            = __VdlyVal__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v7;
    }
    if (__VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v8) {
        vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__c[1U] 
            = __VdlyVal__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v8;
        vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__c[0U] = 0U;
    }
    if (__VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v10) {
        vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__c[0U] 
            = __VdlyVal__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v10;
    }
    if (__VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v11) {
        vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__c[0U] = 0U;
    }
    if (__VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v12) {
        vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__c[1U] = 0U;
    }
    if (__VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v13) {
        vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__c[2U] = 0U;
    }
    if (__VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v14) {
        vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__c[3U] = 0U;
    }
    if (__VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v15) {
        vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__c[4U] = 0U;
    }
    if (__VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v16) {
        vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__c[5U] = 0U;
    }
    if (__VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v17) {
        vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__c[6U] = 0U;
    }
    if (__VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v18) {
        vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__c[7U] = 0U;
    }
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__wh 
        = __Vdly__edges__BRA__2__KET____DOT__u_hebb__DOT__wh;
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__hl_cnt 
        = __Vdly__edges__BRA__3__KET____DOT__u_hebb__DOT__hl_cnt;
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__age 
        = __Vdly__edges__BRA__3__KET____DOT__u_hebb__DOT__age;
    if (__VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v0) {
        vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__c[7U] 
            = __VdlyVal__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v0;
    }
    if (__VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v1) {
        vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__c[__VdlyDim0__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v1] 
            = __VdlyVal__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v1;
    }
    if (__VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v2) {
        vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__c[7U] 
            = __VdlyVal__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v2;
    }
    if (__VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v3) {
        vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__c[6U] 
            = __VdlyVal__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v3;
    }
    if (__VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v4) {
        vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__c[5U] 
            = __VdlyVal__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v4;
    }
    if (__VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v5) {
        vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__c[4U] 
            = __VdlyVal__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v5;
    }
    if (__VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v6) {
        vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__c[3U] 
            = __VdlyVal__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v6;
    }
    if (__VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v7) {
        vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__c[2U] 
            = __VdlyVal__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v7;
    }
    if (__VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v8) {
        vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__c[1U] 
            = __VdlyVal__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v8;
        vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__c[0U] = 0U;
    }
    if (__VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v10) {
        vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__c[0U] 
            = __VdlyVal__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v10;
    }
    if (__VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v11) {
        vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__c[0U] = 0U;
    }
    if (__VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v12) {
        vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__c[1U] = 0U;
    }
    if (__VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v13) {
        vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__c[2U] = 0U;
    }
    if (__VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v14) {
        vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__c[3U] = 0U;
    }
    if (__VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v15) {
        vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__c[4U] = 0U;
    }
    if (__VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v16) {
        vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__c[5U] = 0U;
    }
    if (__VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v17) {
        vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__c[6U] = 0U;
    }
    if (__VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v18) {
        vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__c[7U] = 0U;
    }
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__wh 
        = __Vdly__edges__BRA__3__KET____DOT__u_hebb__DOT__wh;
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__hl_cnt 
        = __Vdly__edges__BRA__0__KET____DOT__u_hebb__DOT__hl_cnt;
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__age 
        = __Vdly__edges__BRA__0__KET____DOT__u_hebb__DOT__age;
    if (__VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v0) {
        vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__c[7U] 
            = __VdlyVal__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v0;
    }
    if (__VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v1) {
        vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__c[__VdlyDim0__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v1] 
            = __VdlyVal__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v1;
    }
    if (__VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v2) {
        vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__c[7U] 
            = __VdlyVal__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v2;
    }
    if (__VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v3) {
        vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__c[6U] 
            = __VdlyVal__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v3;
    }
    if (__VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v4) {
        vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__c[5U] 
            = __VdlyVal__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v4;
    }
    if (__VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v5) {
        vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__c[4U] 
            = __VdlyVal__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v5;
    }
    if (__VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v6) {
        vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__c[3U] 
            = __VdlyVal__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v6;
    }
    if (__VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v7) {
        vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__c[2U] 
            = __VdlyVal__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v7;
    }
    if (__VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v8) {
        vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__c[1U] 
            = __VdlyVal__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v8;
        vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__c[0U] = 0U;
    }
    if (__VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v10) {
        vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__c[0U] 
            = __VdlyVal__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v10;
    }
    if (__VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v11) {
        vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__c[0U] = 0U;
    }
    if (__VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v12) {
        vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__c[1U] = 0U;
    }
    if (__VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v13) {
        vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__c[2U] = 0U;
    }
    if (__VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v14) {
        vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__c[3U] = 0U;
    }
    if (__VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v15) {
        vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__c[4U] = 0U;
    }
    if (__VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v16) {
        vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__c[5U] = 0U;
    }
    if (__VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v17) {
        vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__c[6U] = 0U;
    }
    if (__VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v18) {
        vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__c[7U] = 0U;
    }
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__wh 
        = __Vdly__edges__BRA__0__KET____DOT__u_hebb__DOT__wh;
    vlSelfRef.u_df__DOT__o_eta_f = vlSelfRef.u_df__DOT__dial
        [0U];
    vlSelfRef.d_eta_f = vlSelfRef.u_df__DOT__dial[0U];
    vlSelfRef.u_df__DOT__o_eta_s = vlSelfRef.u_df__DOT__dial
        [1U];
    vlSelfRef.d_eta_s = vlSelfRef.u_df__DOT__dial[1U];
    vlSelfRef.u_df__DOT__o_thresh = vlSelfRef.u_df__DOT__dial
        [5U];
    vlSelfRef.u_df__DOT__o_refr = vlSelfRef.u_df__DOT__dial
        [6U];
    vlSelfRef.u_df__DOT__o_cosmin = vlSelfRef.u_df__DOT__dial
        [7U];
    vlSelfRef.d_cosmin = vlSelfRef.u_df__DOT__dial[7U];
    vlSelfRef.u_df__DOT__o_hl = vlSelfRef.u_df__DOT__dial
        [0xaU];
    vlSelfRef.u_df__DOT__o_floor = vlSelfRef.u_df__DOT__dial
        [0xcU];
    vlSelfRef.u_df__DOT__o_kf = (0xfU & vlSelfRef.u_df__DOT__dial
                                 [2U]);
    vlSelfRef.u_df__DOT__o_ks = (0xfU & vlSelfRef.u_df__DOT__dial
                                 [3U]);
    vlSelfRef.d_ka = (0xfU & vlSelfRef.u_df__DOT__dial
                      [4U]);
    vlSelfRef.d_hl = vlSelfRef.u_df__DOT__dial[0xaU];
    vlSelfRef.d_kle = (0xfU & vlSelfRef.u_df__DOT__dial
                       [0xbU]);
    vlSelfRef.d_floor = vlSelfRef.u_df__DOT__dial[0xcU];
    vlSelfRef.d_qleak = (0xfU & vlSelfRef.u_df__DOT__dial
                         [0xfU]);
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__hlth 
        = vlSelfRef.u_df__DOT__dial[0xaU];
    vlSelfRef.d_rqen = (1U & (vlSelfRef.u_df__DOT__dial
                              [0xeU] >> 0xfU));
    vlSelfRef.d_mode = (1U & vlSelfRef.u_df__DOT__dial
                        [9U]);
    vlSelfRef.d_p0e = (0x1fU & vlSelfRef.u_df__DOT__dial
                       [8U]);
    vlSelfRef.d_qdw = (0xfU & vlSelfRef.u_df__DOT__dial
                       [0xeU]);
    vlSelfRef.u_egbuf__DOT__s_ready = (1U & (~ (IData)(vlSelfRef.u_egbuf__DOT__b_v)));
    vlSelfRef.u_egbuf__DOT__m_valid = vlSelfRef.u_egbuf__DOT__a_v;
    vlSelfRef.li_valid_w = vlSelfRef.u_egbuf__DOT__a_v;
    vlSelfRef.li_op_w = (7U & (vlSelfRef.u_egbuf__DOT__a_q[2U] 
                               >> 8U));
    vlSelfRef.li_src_w = (0xfU & (vlSelfRef.u_egbuf__DOT__a_q[2U] 
                                  >> 4U));
    vlSelfRef.li_dst_w = (0xfU & vlSelfRef.u_egbuf__DOT__a_q[2U]);
    vlSelfRef.li_a0_w = (vlSelfRef.u_egbuf__DOT__a_q[1U] 
                         >> 0x10U);
    vlSelfRef.li_a1_w = (0xffffU & vlSelfRef.u_egbuf__DOT__a_q[1U]);
    vlSelfRef.li_a2_w = (vlSelfRef.u_egbuf__DOT__a_q[0U] 
                         >> 0x10U);
    vlSelfRef.li_dat_w = (0xffffU & vlSelfRef.u_egbuf__DOT__a_q[0U]);
    vlSelfRef.u_inbuf__DOT__m_valid = vlSelfRef.u_inbuf__DOT__a_v;
    vlSelfRef.u_core__DOT__ci_a0_rsvd = (vlSelfRef.u_inbuf__DOT__a_q[1U] 
                                         >> 0x14U);
    vlSelfRef.u_inbuf__DOT__m_dst = (0xfU & vlSelfRef.u_inbuf__DOT__a_q[2U]);
    vlSelfRef.ld_ready = (1U & (~ (IData)(vlSelfRef.u_inbuf__DOT__b_v)));
    vlSelfRef.u_core__DOT__o_ftrace = vlSelfRef.u_core__DOT__u_eg__DOT__f;
    vlSelfRef.u_core__DOT__u_eg__DOT__o_f = vlSelfRef.u_core__DOT__u_eg__DOT__f;
    vlSelfRef.w_ftrace = vlSelfRef.u_core__DOT__u_eg__DOT__f;
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__hlc 
        = (0x1ffffU & ((IData)(1U) + (IData)(vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__hl_cnt)));
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__agen 
        = ((IData)(1U) + vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__age);
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__ridx32 
        = vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__ridx;
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__g_lad_sat__DOT__sat 
        = (1U & (vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__acc 
                 >> 0x10U));
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__whs 
        = ((0xffU < (IData)(vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__wh))
            ? 0xffffU : (0xffffU & VL_SHIFTL_III(16,16,32, (IData)(vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__wh), 8U)));
    __Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__32__v 
        = vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__wh;
    __Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__32__Vfuncout = 0U;
    if ((1U & (IData)(__Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__32__v))) {
        __Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__32__Vfuncout = 0U;
    }
    if ((2U & (IData)(__Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__32__v))) {
        __Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__32__Vfuncout = 1U;
    }
    if ((4U & (IData)(__Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__32__v))) {
        __Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__32__Vfuncout = 2U;
    }
    if ((8U & (IData)(__Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__32__v))) {
        __Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__32__Vfuncout = 3U;
    }
    if ((0x10U & (IData)(__Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__32__v))) {
        __Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__32__Vfuncout = 4U;
    }
    if ((0x20U & (IData)(__Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__32__v))) {
        __Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__32__Vfuncout = 5U;
    }
    if ((0x40U & (IData)(__Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__32__v))) {
        __Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__32__Vfuncout = 6U;
    }
    if ((0x80U & (IData)(__Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__32__v))) {
        __Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__32__Vfuncout = 7U;
    }
    if ((0x100U & (IData)(__Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__32__v))) {
        __Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__32__Vfuncout = 8U;
    }
    if ((0x200U & (IData)(__Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__32__v))) {
        __Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__32__Vfuncout = 9U;
    }
    if ((0x400U & (IData)(__Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__32__v))) {
        __Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__32__Vfuncout = 0xaU;
    }
    if ((0x800U & (IData)(__Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__32__v))) {
        __Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__32__Vfuncout = 0xbU;
    }
    if ((0x1000U & (IData)(__Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__32__v))) {
        __Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__32__Vfuncout = 0xcU;
    }
    if ((0x2000U & (IData)(__Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__32__v))) {
        __Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__32__Vfuncout = 0xdU;
    }
    if ((0x4000U & (IData)(__Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__32__v))) {
        __Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__32__Vfuncout = 0xeU;
    }
    if ((0x8000U & (IData)(__Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__32__v))) {
        __Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__32__Vfuncout = 0xfU;
    }
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__wmsb 
        = __Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__32__Vfuncout;
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__hlc 
        = (0x1ffffU & ((IData)(1U) + (IData)(vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__hl_cnt)));
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__agen 
        = ((IData)(1U) + vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__age);
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__ridx32 
        = vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__ridx;
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__g_lad_sat__DOT__sat 
        = (1U & (vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__acc 
                 >> 0x10U));
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__whs 
        = ((0xffU < (IData)(vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__wh))
            ? 0xffffU : (0xffffU & VL_SHIFTL_III(16,16,32, (IData)(vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__wh), 8U)));
    __Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__33__v 
        = vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__wh;
    __Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__33__Vfuncout = 0U;
    if ((1U & (IData)(__Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__33__v))) {
        __Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__33__Vfuncout = 0U;
    }
    if ((2U & (IData)(__Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__33__v))) {
        __Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__33__Vfuncout = 1U;
    }
    if ((4U & (IData)(__Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__33__v))) {
        __Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__33__Vfuncout = 2U;
    }
    if ((8U & (IData)(__Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__33__v))) {
        __Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__33__Vfuncout = 3U;
    }
    if ((0x10U & (IData)(__Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__33__v))) {
        __Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__33__Vfuncout = 4U;
    }
    if ((0x20U & (IData)(__Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__33__v))) {
        __Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__33__Vfuncout = 5U;
    }
    if ((0x40U & (IData)(__Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__33__v))) {
        __Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__33__Vfuncout = 6U;
    }
    if ((0x80U & (IData)(__Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__33__v))) {
        __Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__33__Vfuncout = 7U;
    }
    if ((0x100U & (IData)(__Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__33__v))) {
        __Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__33__Vfuncout = 8U;
    }
    if ((0x200U & (IData)(__Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__33__v))) {
        __Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__33__Vfuncout = 9U;
    }
    if ((0x400U & (IData)(__Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__33__v))) {
        __Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__33__Vfuncout = 0xaU;
    }
    if ((0x800U & (IData)(__Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__33__v))) {
        __Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__33__Vfuncout = 0xbU;
    }
    if ((0x1000U & (IData)(__Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__33__v))) {
        __Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__33__Vfuncout = 0xcU;
    }
    if ((0x2000U & (IData)(__Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__33__v))) {
        __Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__33__Vfuncout = 0xdU;
    }
    if ((0x4000U & (IData)(__Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__33__v))) {
        __Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__33__Vfuncout = 0xeU;
    }
    if ((0x8000U & (IData)(__Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__33__v))) {
        __Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__33__Vfuncout = 0xfU;
    }
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__wmsb 
        = __Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__33__Vfuncout;
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__hlc 
        = (0x1ffffU & ((IData)(1U) + (IData)(vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__hl_cnt)));
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__agen 
        = ((IData)(1U) + vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__age);
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__ridx32 
        = vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__ridx;
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__g_lad_sat__DOT__sat 
        = (1U & (vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__acc 
                 >> 0x10U));
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__whs 
        = ((0xffU < (IData)(vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__wh))
            ? 0xffffU : (0xffffU & VL_SHIFTL_III(16,16,32, (IData)(vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__wh), 8U)));
    __Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__34__v 
        = vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__wh;
    __Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__34__Vfuncout = 0U;
    if ((1U & (IData)(__Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__34__v))) {
        __Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__34__Vfuncout = 0U;
    }
    if ((2U & (IData)(__Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__34__v))) {
        __Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__34__Vfuncout = 1U;
    }
    if ((4U & (IData)(__Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__34__v))) {
        __Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__34__Vfuncout = 2U;
    }
    if ((8U & (IData)(__Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__34__v))) {
        __Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__34__Vfuncout = 3U;
    }
    if ((0x10U & (IData)(__Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__34__v))) {
        __Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__34__Vfuncout = 4U;
    }
    if ((0x20U & (IData)(__Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__34__v))) {
        __Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__34__Vfuncout = 5U;
    }
    if ((0x40U & (IData)(__Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__34__v))) {
        __Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__34__Vfuncout = 6U;
    }
    if ((0x80U & (IData)(__Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__34__v))) {
        __Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__34__Vfuncout = 7U;
    }
    if ((0x100U & (IData)(__Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__34__v))) {
        __Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__34__Vfuncout = 8U;
    }
    if ((0x200U & (IData)(__Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__34__v))) {
        __Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__34__Vfuncout = 9U;
    }
    if ((0x400U & (IData)(__Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__34__v))) {
        __Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__34__Vfuncout = 0xaU;
    }
    if ((0x800U & (IData)(__Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__34__v))) {
        __Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__34__Vfuncout = 0xbU;
    }
    if ((0x1000U & (IData)(__Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__34__v))) {
        __Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__34__Vfuncout = 0xcU;
    }
    if ((0x2000U & (IData)(__Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__34__v))) {
        __Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__34__Vfuncout = 0xdU;
    }
    if ((0x4000U & (IData)(__Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__34__v))) {
        __Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__34__Vfuncout = 0xeU;
    }
    if ((0x8000U & (IData)(__Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__34__v))) {
        __Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__34__Vfuncout = 0xfU;
    }
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__wmsb 
        = __Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__34__Vfuncout;
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__hlc 
        = (0x1ffffU & ((IData)(1U) + (IData)(vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__hl_cnt)));
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__agen 
        = ((IData)(1U) + vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__age);
    vlSelfRef.done_vec = (((IData)(vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__o_done) 
                           << 3U) | (((IData)(vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__o_done) 
                                      << 2U) | (((IData)(vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__o_done) 
                                                 << 1U) 
                                                | (IData)(vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__o_done))));
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__ridx32 
        = vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__ridx;
    vlSelfRef.ovf_vec = (((IData)(vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__o_ovf) 
                          << 3U) | (((IData)(vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__o_ovf) 
                                     << 2U) | (((IData)(vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__o_ovf) 
                                                << 1U) 
                                               | (IData)(vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__o_ovf))));
    vlSelfRef.w_flat = (((QData)((IData)(vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__o_w)) 
                         << 0x30U) | (((QData)((IData)(
                                                       (((IData)(vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__o_w) 
                                                         << 0x10U) 
                                                        | (IData)(vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__o_w)))) 
                                       << 0x10U) | (QData)((IData)(vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__o_w))));
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__g_lad_sat__DOT__sat 
        = (1U & (vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__acc 
                 >> 0x10U));
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__whs 
        = ((0xffU < (IData)(vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__wh))
            ? 0xffffU : (0xffffU & VL_SHIFTL_III(16,16,32, (IData)(vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__wh), 8U)));
    __Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__31__v 
        = vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__wh;
    __Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__31__Vfuncout = 0U;
    if ((1U & (IData)(__Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__31__v))) {
        __Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__31__Vfuncout = 0U;
    }
    if ((2U & (IData)(__Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__31__v))) {
        __Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__31__Vfuncout = 1U;
    }
    if ((4U & (IData)(__Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__31__v))) {
        __Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__31__Vfuncout = 2U;
    }
    if ((8U & (IData)(__Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__31__v))) {
        __Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__31__Vfuncout = 3U;
    }
    if ((0x10U & (IData)(__Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__31__v))) {
        __Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__31__Vfuncout = 4U;
    }
    if ((0x20U & (IData)(__Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__31__v))) {
        __Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__31__Vfuncout = 5U;
    }
    if ((0x40U & (IData)(__Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__31__v))) {
        __Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__31__Vfuncout = 6U;
    }
    if ((0x80U & (IData)(__Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__31__v))) {
        __Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__31__Vfuncout = 7U;
    }
    if ((0x100U & (IData)(__Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__31__v))) {
        __Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__31__Vfuncout = 8U;
    }
    if ((0x200U & (IData)(__Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__31__v))) {
        __Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__31__Vfuncout = 9U;
    }
    if ((0x400U & (IData)(__Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__31__v))) {
        __Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__31__Vfuncout = 0xaU;
    }
    if ((0x800U & (IData)(__Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__31__v))) {
        __Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__31__Vfuncout = 0xbU;
    }
    if ((0x1000U & (IData)(__Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__31__v))) {
        __Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__31__Vfuncout = 0xcU;
    }
    if ((0x2000U & (IData)(__Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__31__v))) {
        __Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__31__Vfuncout = 0xdU;
    }
    if ((0x4000U & (IData)(__Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__31__v))) {
        __Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__31__Vfuncout = 0xeU;
    }
    if ((0x8000U & (IData)(__Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__31__v))) {
        __Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__31__Vfuncout = 0xfU;
    }
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__wmsb 
        = __Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__31__Vfuncout;
    vlSelfRef.d_kf = vlSelfRef.u_df__DOT__o_kf;
    vlSelfRef.d_ks = vlSelfRef.u_df__DOT__o_ks;
    vlSelfRef.u_core__DOT__d_ka = vlSelfRef.d_ka;
    vlSelfRef.u_df__DOT__o_ka = vlSelfRef.d_ka;
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__i_hl 
        = vlSelfRef.d_hl;
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__i_hl 
        = vlSelfRef.d_hl;
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__i_hl 
        = vlSelfRef.d_hl;
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__i_hl 
        = vlSelfRef.d_hl;
    vlSelfRef.u_df__DOT__o_kle = vlSelfRef.d_kle;
    vlSelfRef.u_core__DOT__d_kle = vlSelfRef.d_kle;
    vlSelfRef.u_core__DOT__u_eg__DOT__fleak = (0xffffU 
                                               & ((IData)(vlSelfRef.u_core__DOT__u_eg__DOT__f) 
                                                  - 
                                                  ((IData)(vlSelfRef.u_core__DOT__u_eg__DOT__f) 
                                                   >> (IData)(vlSelfRef.d_kle))));
    vlSelfRef.u_core__DOT__d_floor = vlSelfRef.d_floor;
    vlSelfRef.u_core__DOT__u_eg__DOT__o_gclass = ((
                                                   (0U 
                                                    == (IData)(vlSelfRef.d_floor)) 
                                                   | (0U 
                                                      == (IData)(vlSelfRef.u_core__DOT__u_eg__DOT__f)))
                                                   ? 0U
                                                   : 
                                                  (0xfU 
                                                   & ((IData)(0xfU) 
                                                      - 
                                                      ([&]() {
                        vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__30__v 
                            = vlSelfRef.u_core__DOT__u_eg__DOT__f;
                        vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__30__Vfuncout = 0U;
                        if ((1U & (IData)(vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__30__v))) {
                            vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__30__Vfuncout = 0U;
                        }
                        vlSelfRef.u_core__DOT__u_eg__DOT__msb_idx__Vstatic__j = 1U;
                        if ((2U & (IData)(vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__30__v))) {
                            vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__30__Vfuncout = 1U;
                        }
                        vlSelfRef.u_core__DOT__u_eg__DOT__msb_idx__Vstatic__j = 2U;
                        if ((4U & (IData)(vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__30__v))) {
                            vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__30__Vfuncout = 2U;
                        }
                        vlSelfRef.u_core__DOT__u_eg__DOT__msb_idx__Vstatic__j = 3U;
                        if ((8U & (IData)(vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__30__v))) {
                            vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__30__Vfuncout = 3U;
                        }
                        vlSelfRef.u_core__DOT__u_eg__DOT__msb_idx__Vstatic__j = 4U;
                        if ((0x10U & (IData)(vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__30__v))) {
                            vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__30__Vfuncout = 4U;
                        }
                        vlSelfRef.u_core__DOT__u_eg__DOT__msb_idx__Vstatic__j = 5U;
                        if ((0x20U & (IData)(vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__30__v))) {
                            vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__30__Vfuncout = 5U;
                        }
                        vlSelfRef.u_core__DOT__u_eg__DOT__msb_idx__Vstatic__j = 6U;
                        if ((0x40U & (IData)(vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__30__v))) {
                            vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__30__Vfuncout = 6U;
                        }
                        vlSelfRef.u_core__DOT__u_eg__DOT__msb_idx__Vstatic__j = 7U;
                        if ((0x80U & (IData)(vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__30__v))) {
                            vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__30__Vfuncout = 7U;
                        }
                        vlSelfRef.u_core__DOT__u_eg__DOT__msb_idx__Vstatic__j = 8U;
                        if ((0x100U & (IData)(vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__30__v))) {
                            vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__30__Vfuncout = 8U;
                        }
                        vlSelfRef.u_core__DOT__u_eg__DOT__msb_idx__Vstatic__j = 9U;
                        if ((0x200U & (IData)(vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__30__v))) {
                            vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__30__Vfuncout = 9U;
                        }
                        vlSelfRef.u_core__DOT__u_eg__DOT__msb_idx__Vstatic__j = 0xaU;
                        if ((0x400U & (IData)(vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__30__v))) {
                            vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__30__Vfuncout = 0xaU;
                        }
                        vlSelfRef.u_core__DOT__u_eg__DOT__msb_idx__Vstatic__j = 0xbU;
                        if ((0x800U & (IData)(vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__30__v))) {
                            vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__30__Vfuncout = 0xbU;
                        }
                        vlSelfRef.u_core__DOT__u_eg__DOT__msb_idx__Vstatic__j = 0xcU;
                        if ((0x1000U & (IData)(vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__30__v))) {
                            vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__30__Vfuncout = 0xcU;
                        }
                        vlSelfRef.u_core__DOT__u_eg__DOT__msb_idx__Vstatic__j = 0xdU;
                        if ((0x2000U & (IData)(vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__30__v))) {
                            vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__30__Vfuncout = 0xdU;
                        }
                        vlSelfRef.u_core__DOT__u_eg__DOT__msb_idx__Vstatic__j = 0xeU;
                        if ((0x4000U & (IData)(vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__30__v))) {
                            vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__30__Vfuncout = 0xeU;
                        }
                        vlSelfRef.u_core__DOT__u_eg__DOT__msb_idx__Vstatic__j = 0xfU;
                        if ((0x8000U & (IData)(vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__30__v))) {
                            vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__30__Vfuncout = 0xfU;
                        }
                        vlSelfRef.u_core__DOT__u_eg__DOT__msb_idx__Vstatic__j = 0x10U;
                    }(), (IData)(vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__30__Vfuncout)))));
    vlSelfRef.u_df__DOT__o_qleak = vlSelfRef.d_qleak;
    vlSelfRef.u_core__DOT__d_qleak = vlSelfRef.d_qleak;
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__hlth 
        = vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__hlth;
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__hlth 
        = vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__hlth;
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__hlth 
        = vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__hlth;
    vlSelfRef.u_df__DOT__o_rqen = vlSelfRef.d_rqen;
    vlSelfRef.u_core__DOT__d_rqen = vlSelfRef.d_rqen;
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__i_mode 
        = vlSelfRef.d_mode;
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__i_mode 
        = vlSelfRef.d_mode;
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__i_mode 
        = vlSelfRef.d_mode;
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__i_mode 
        = vlSelfRef.d_mode;
    vlSelfRef.u_df__DOT__o_mode = vlSelfRef.d_mode;
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__i_p0e 
        = vlSelfRef.d_p0e;
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__i_p0e 
        = vlSelfRef.d_p0e;
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__i_p0e 
        = vlSelfRef.d_p0e;
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__i_p0e 
        = vlSelfRef.d_p0e;
    vlSelfRef.u_df__DOT__o_p0e = vlSelfRef.d_p0e;
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__p0 
        = ((IData)(1U) << (IData)(vlSelfRef.d_p0e));
    vlSelfRef.u_df__DOT__o_qdw = vlSelfRef.d_qdw;
    vlSelfRef.u_core__DOT__d_qdw = vlSelfRef.d_qdw;
    vlSelfRef.eg_s_ready = vlSelfRef.u_egbuf__DOT__s_ready;
    vlSelfRef.u_rp__DOT__li_valid = vlSelfRef.li_valid_w;
    vlSelfRef.u_rp__DOT__li_op = vlSelfRef.li_op_w;
    vlSelfRef.u_egbuf__DOT__m_op = vlSelfRef.li_op_w;
    vlSelfRef.u_rp__DOT__li_src = vlSelfRef.li_src_w;
    vlSelfRef.u_egbuf__DOT__m_src = vlSelfRef.li_src_w;
    vlSelfRef.u_rp__DOT__li_dst = vlSelfRef.li_dst_w;
    vlSelfRef.u_egbuf__DOT__m_dst = vlSelfRef.li_dst_w;
    vlSelfRef.u_rp__DOT__li_a0 = vlSelfRef.li_a0_w;
    vlSelfRef.u_egbuf__DOT__m_a0 = vlSelfRef.li_a0_w;
    vlSelfRef.u_rp__DOT__li_a1 = vlSelfRef.li_a1_w;
    vlSelfRef.u_egbuf__DOT__m_a1 = vlSelfRef.li_a1_w;
    vlSelfRef.u_rp__DOT__li_a2 = vlSelfRef.li_a2_w;
    vlSelfRef.u_egbuf__DOT__m_a2 = vlSelfRef.li_a2_w;
    vlSelfRef.u_rp__DOT__li_dat = vlSelfRef.li_dat_w;
    vlSelfRef.u_egbuf__DOT__m_dat = vlSelfRef.li_dat_w;
    vlSelfRef.w_indst = vlSelfRef.u_inbuf__DOT__m_dst;
    vlSelfRef.u_rp__DOT__ld_ready = vlSelfRef.ld_ready;
    vlSelfRef.u_inbuf__DOT__s_ready = vlSelfRef.ld_ready;
    vlSelfRef.u_df__DOT__i_probe = vlSelfRef.w_ftrace;
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__hlend 
        = (vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__hlc 
           >= vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__hlth);
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__rsh 
        = ((IData)(8U) - vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__ridx32);
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__lad 
        = ((IData)(vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__g_lad_sat__DOT__sat)
            ? 0xffffU : (0xffffU & vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__acc));
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__shl2 
        = (0x1fU & ((IData)(vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__wmsb) 
                    + (IData)(vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__wmsb)));
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__hlend 
        = (vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__hlc 
           >= vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__hlth);
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__rsh 
        = ((IData)(8U) - vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__ridx32);
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__lad 
        = ((IData)(vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__g_lad_sat__DOT__sat)
            ? 0xffffU : (0xffffU & vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__acc));
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__shl2 
        = (0x1fU & ((IData)(vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__wmsb) 
                    + (IData)(vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__wmsb)));
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__hlend 
        = (vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__hlc 
           >= vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__hlth);
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__rsh 
        = ((IData)(8U) - vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__ridx32);
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__lad 
        = ((IData)(vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__g_lad_sat__DOT__sat)
            ? 0xffffU : (0xffffU & vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__acc));
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__shl2 
        = (0x1fU & ((IData)(vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__wmsb) 
                    + (IData)(vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__wmsb)));
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__hlend 
        = (vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__hlc 
           >= vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__hlth);
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__rsh 
        = ((IData)(8U) - vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__ridx32);
    vlSelfRef.o_ovf = (0U != (IData)(vlSelfRef.ovf_vec));
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__lad 
        = ((IData)(vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__g_lad_sat__DOT__sat)
            ? 0xffffU : (0xffffU & vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__acc));
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__shl2 
        = (0x1fU & ((IData)(vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__wmsb) 
                    + (IData)(vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__wmsb)));
    vlSelfRef.u_core__DOT__tick_pend = __Vdly__u_core__DOT__tick_pend;
    vlSelfRef.u_core__DOT__refr = __Vdly__u_core__DOT__refr;
    vlSelfRef.u_core__DOT__eidx = __Vdly__u_core__DOT__eidx;
    vlSelfRef.u_core__DOT__wacc = __Vdly__u_core__DOT__wacc;
    vlSelfRef.hb_done = (0U != (IData)(vlSelfRef.done_vec));
    vlSelfRef.d_refr = vlSelfRef.u_df__DOT__dial[6U];
    vlSelfRef.d_thresh = vlSelfRef.u_df__DOT__dial[5U];
    vlSelfRef.df_rstb = vlSelfRef.u_df__DOT__o_rstb;
    vlSelfRef.df_rdata = vlSelfRef.u_df__DOT__o_rdata;
    vlSelfRef.ci_valid = vlSelfRef.u_inbuf__DOT__a_v;
    vlSelfRef.u_core__DOT__eg_live = ((0U == vlSelfRef.u_df__DOT__dial
                                       [0xcU]) | ((IData)(vlSelfRef.u_core__DOT__u_eg__DOT__f) 
                                                  >= 
                                                  vlSelfRef.u_df__DOT__dial
                                                  [0xcU]));
    vlSelfRef.ci_src = (0xfU & (vlSelfRef.u_inbuf__DOT__a_q[2U] 
                                >> 4U));
    vlSelfRef.ci_a0 = (vlSelfRef.u_inbuf__DOT__a_q[1U] 
                       >> 0x10U);
    vlSelfRef.ci_a1 = (0xffffU & vlSelfRef.u_inbuf__DOT__a_q[1U]);
    vlSelfRef.ci_a2 = (vlSelfRef.u_inbuf__DOT__a_q[0U] 
                       >> 0x10U);
    vlSelfRef.ci_dat = (0xffffU & vlSelfRef.u_inbuf__DOT__a_q[0U]);
    vlSelfRef.ci_op = (7U & (vlSelfRef.u_inbuf__DOT__a_q[2U] 
                             >> 8U));
    vlSelfRef.u_core__DOT__state = __Vdly__u_core__DOT__state;
    if (__VdlySet__u_core__DOT__etab__v0) {
        vlSelfRef.u_core__DOT__etab[__VdlyDim0__u_core__DOT__etab__v0] 
            = __VdlyVal__u_core__DOT__etab__v0;
        vlSelfRef.u_core__DOT__ev[__VdlyDim0__u_core__DOT__ev__v0] = 1U;
    }
    if (__VdlySet__u_core__DOT__etab__v1) {
        vlSelfRef.u_core__DOT__etab[0U] = 0U;
        vlSelfRef.u_core__DOT__ev[0U] = 0U;
        vlSelfRef.u_core__DOT__etab[1U] = 0U;
        vlSelfRef.u_core__DOT__ev[1U] = 0U;
        vlSelfRef.u_core__DOT__etab[2U] = 0U;
        vlSelfRef.u_core__DOT__ev[2U] = 0U;
        vlSelfRef.u_core__DOT__etab[3U] = 0U;
        vlSelfRef.u_core__DOT__ev[3U] = 0U;
    }
    vlSelfRef.u_core__DOT__ci_ready = __Vdly__u_core__DOT__ci_ready;
    vlSelfRef.u_core__DOT__lx_valid = __Vdly__u_core__DOT__lx_valid;
    vlSelfRef.u_core__DOT__act = __Vdly__u_core__DOT__act;
    vlSelfRef.u_core__DOT__lo_valid = __Vdly__u_core__DOT__lo_valid;
    vlSelfRef.u_core__DOT__u_eg__DOT__i_kle = vlSelfRef.u_core__DOT__d_kle;
    vlSelfRef.u_core__DOT__u_eg__DOT__fsnap = (((IData)(vlSelfRef.u_core__DOT__u_eg__DOT__fleak) 
                                                <= 
                                                vlSelfRef.u_df__DOT__dial
                                                [0xcU]) 
                                               | ((1U 
                                                   >= (IData)(vlSelfRef.u_core__DOT__u_eg__DOT__fleak)) 
                                                  | ((IData)(vlSelfRef.u_core__DOT__u_eg__DOT__fleak) 
                                                     >= (IData)(vlSelfRef.u_core__DOT__u_eg__DOT__f))));
    vlSelfRef.u_core__DOT__u_eg__DOT__i_floor = vlSelfRef.u_core__DOT__d_floor;
    vlSelfRef.u_core__DOT__eg_gclass = vlSelfRef.u_core__DOT__u_eg__DOT__o_gclass;
    vlSelfRef.u_core__DOT__u_rq__DOT__i_qleak = vlSelfRef.u_core__DOT__d_qleak;
    vlSelfRef.u_core__DOT__u_rq__DOT__i_en = vlSelfRef.u_core__DOT__d_rqen;
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__p0 
        = vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__p0;
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__p0 
        = vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__p0;
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__p0 
        = vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__p0;
    vlSelfRef.u_core__DOT__u_rq__DOT__i_qdw = vlSelfRef.u_core__DOT__d_qdw;
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__addw 
        = (0x1ffffU & VL_SHIFTL_III(17,17,32, vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__c
                                    [(7U & (IData)(vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__ridx))], vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__rsh));
    if (vlSelfRef.d_mode) {
        vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__eng 
            = vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__whs;
        vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__eng 
            = vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__whs;
        vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__eng 
            = vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__whs;
        vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__eng 
            = vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__whs;
    } else {
        vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__eng 
            = vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__lad;
        vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__eng 
            = vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__lad;
        vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__eng 
            = vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__lad;
        vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__eng 
            = vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__lad;
    }
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__ivr 
        = (vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__p0 
           >> (IData)(vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__shl2));
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__addw 
        = (0x1ffffU & VL_SHIFTL_III(17,17,32, vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__c
                                    [(7U & (IData)(vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__ridx))], vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__rsh));
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__ivr 
        = (vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__p0 
           >> (IData)(vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__shl2));
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__addw 
        = (0x1ffffU & VL_SHIFTL_III(17,17,32, vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__c
                                    [(7U & (IData)(vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__ridx))], vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__rsh));
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__ivr 
        = (vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__p0 
           >> (IData)(vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__shl2));
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__addw 
        = (0x1ffffU & VL_SHIFTL_III(17,17,32, vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__c
                                    [(7U & (IData)(vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__ridx))], vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__rsh));
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__ivr 
        = (vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__p0 
           >> (IData)(vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__shl2));
    vlSelfRef.u_core__DOT__hb_done = vlSelfRef.hb_done;
    vlSelfRef.u_core__DOT__d_refr = vlSelfRef.d_refr;
    vlSelfRef.u_core__DOT__d_thresh = vlSelfRef.d_thresh;
    vlSelfRef.u_core__DOT__df_rstb = vlSelfRef.df_rstb;
    vlSelfRef.u_core__DOT__df_rdata = vlSelfRef.df_rdata;
    vlSelfRef.u_core__DOT__ci_valid = vlSelfRef.ci_valid;
    vlSelfRef.u_core__DOT__u_eg__DOT__i_fire = vlSelfRef.u_core__DOT__eg_fire;
    vlSelfRef.u_core__DOT__eff_pe = (((QData)((IData)(
                                                      (7U 
                                                       & (- (IData)(
                                                                    (1U 
                                                                     & (IData)(
                                                                               (vlSelfRef.u_core__DOT__eff_p 
                                                                                >> 0x20U)))))))) 
                                      << 0x21U) | vlSelfRef.u_core__DOT__eff_p);
    vlSelfRef.u_core__DOT__u_eg__DOT__o_live = vlSelfRef.u_core__DOT__eg_live;
    vlSelfRef.w_cid = vlSelfRef.u_core__DOT__cell_id;
    vlSelfRef.w_bound = vlSelfRef.u_core__DOT__bound;
    vlSelfRef.u_core__DOT__ci_src = vlSelfRef.ci_src;
    vlSelfRef.u_inbuf__DOT__m_src = vlSelfRef.ci_src;
    vlSelfRef.u_core__DOT__ci_a0 = vlSelfRef.ci_a0;
    vlSelfRef.u_inbuf__DOT__m_a0 = vlSelfRef.ci_a0;
    vlSelfRef.u_core__DOT__ci_a1 = vlSelfRef.ci_a1;
    vlSelfRef.u_inbuf__DOT__m_a1 = vlSelfRef.ci_a1;
    vlSelfRef.u_core__DOT__ci_a2 = vlSelfRef.ci_a2;
    vlSelfRef.u_inbuf__DOT__m_a2 = vlSelfRef.ci_a2;
    vlSelfRef.u_core__DOT__ci_dat = vlSelfRef.ci_dat;
    vlSelfRef.u_inbuf__DOT__m_dat = vlSelfRef.ci_dat;
    vlSelfRef.u_core__DOT__ci_op = vlSelfRef.ci_op;
    vlSelfRef.u_inbuf__DOT__m_op = vlSelfRef.ci_op;
    vlSelfRef.df_rd = vlSelfRef.u_core__DOT__df_rd;
    vlSelfRef.u_core__DOT__eg_tick = (0x11U == (IData)(vlSelfRef.u_core__DOT__state));
    vlSelfRef.df_wr = vlSelfRef.u_core__DOT__df_wr;
    vlSelfRef.df_wr_g = ((IData)(vlSelfRef.i_bdf_wr) 
                         | (IData)(vlSelfRef.u_core__DOT__df_wr));
    vlSelfRef.u_inbuf__DOT__pop = ((IData)(vlSelfRef.u_core__DOT__ci_ready) 
                                   & (IData)(vlSelfRef.u_inbuf__DOT__a_v));
    vlSelfRef.ci_ready_w = vlSelfRef.u_core__DOT__ci_ready;
    vlSelfRef.df_addr = vlSelfRef.u_core__DOT__df_addr;
    if (vlSelfRef.i_bdf_wr) {
        vlSelfRef.df_addr_g = vlSelfRef.i_bdf_addr;
        vlSelfRef.df_wdata_g = vlSelfRef.i_bdf_wdata;
    } else {
        vlSelfRef.df_addr_g = vlSelfRef.u_core__DOT__df_addr;
        vlSelfRef.df_wdata_g = vlSelfRef.u_core__DOT__df_wdata;
    }
    vlSelfRef.df_wdata = vlSelfRef.u_core__DOT__df_wdata;
    vlSelfRef.lx_valid = vlSelfRef.u_core__DOT__lx_valid;
    vlSelfRef.w_act = vlSelfRef.u_core__DOT__act;
    vlSelfRef.u_core__DOT__act_e = (((QData)((IData)(
                                                     (0xfffffU 
                                                      & (- (IData)(
                                                                   (1U 
                                                                    & ((IData)(vlSelfRef.u_core__DOT__act) 
                                                                       >> 0xfU))))))) 
                                     << 0x10U) | (QData)((IData)(vlSelfRef.u_core__DOT__act)));
    vlSelfRef.hb_base = vlSelfRef.u_core__DOT__hb_base;
    vlSelfRef.u_core__DOT__prod_p = (0x1ffffffffULL 
                                     & VL_MULS_QQQ(33, 
                                                   (0x1ffffffffULL 
                                                    & VL_EXTENDS_QI(33,17, (IData)(vlSelfRef.u_core__DOT__eff_w))), 
                                                   (0x1ffffffffULL 
                                                    & VL_EXTENDS_QI(33,16, (IData)(vlSelfRef.u_core__DOT__lr_dat)))));
    vlSelfRef.lx_op = vlSelfRef.u_core__DOT__lx_op;
    vlSelfRef.lx_dst = vlSelfRef.u_core__DOT__lx_dst;
    vlSelfRef.lx_src = vlSelfRef.u_core__DOT__lx_src;
    vlSelfRef.lx_dat = vlSelfRef.u_core__DOT__lx_dat;
    vlSelfRef.lx_a0 = vlSelfRef.u_core__DOT__lx_a0;
    vlSelfRef.lx_a1 = vlSelfRef.u_core__DOT__lx_a1;
    vlSelfRef.lx_a2 = vlSelfRef.u_core__DOT__lx_a2;
    vlSelfRef.lo_op = vlSelfRef.u_core__DOT__lo_op;
    vlSelfRef.lo_dst = vlSelfRef.u_core__DOT__lo_dst;
    vlSelfRef.lo_src = vlSelfRef.u_core__DOT__lo_src;
    vlSelfRef.lo_a0 = vlSelfRef.u_core__DOT__lo_a0;
    vlSelfRef.lo_a1 = vlSelfRef.u_core__DOT__lo_a1;
    vlSelfRef.lo_a2 = vlSelfRef.u_core__DOT__lo_a2;
    vlSelfRef.lo_dat = vlSelfRef.u_core__DOT__lo_dat;
    vlSelfRef.u_core__DOT__rq_tick = (2U == (IData)(vlSelfRef.u_core__DOT__hb_cmd));
    vlSelfRef.hb_cmd = vlSelfRef.u_core__DOT__hb_cmd;
    vlSelfRef.u_core__DOT__rq_train = (5U == (IData)(vlSelfRef.u_core__DOT__hb_cmd));
    vlSelfRef.u_core__DOT__u_rq__DOT__i_gclass = vlSelfRef.u_core__DOT__hb_gcl;
    vlSelfRef.hb_gcl = vlSelfRef.u_core__DOT__hb_gcl;
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__gcl 
        = ((8U <= (IData)(vlSelfRef.u_core__DOT__hb_gcl))
            ? 7U : (IData)(vlSelfRef.u_core__DOT__hb_gcl));
    vlSelfRef.lo_valid = vlSelfRef.u_core__DOT__lo_valid;
    vlSelfRef.lo_grant = (1U & ((~ (IData)(vlSelfRef.u_core__DOT__lo_valid)) 
                                | (IData)(vlSelfRef.u_egbuf__DOT__s_ready)));
    vlSelfRef.lx_grant = ((~ (IData)(vlSelfRef.u_core__DOT__lo_valid)) 
                          & (IData)(vlSelfRef.u_egbuf__DOT__s_ready));
    vlSelfRef.eg_s_valid = ((IData)(vlSelfRef.u_core__DOT__lo_valid) 
                            | (IData)(vlSelfRef.u_core__DOT__lx_valid));
    if (vlSelfRef.u_core__DOT__lo_valid) {
        vlSelfRef.eg_op = vlSelfRef.u_core__DOT__lo_op;
        vlSelfRef.eg_src = vlSelfRef.u_core__DOT__lo_src;
        vlSelfRef.eg_dst = vlSelfRef.u_core__DOT__lo_dst;
        vlSelfRef.eg_a0 = vlSelfRef.u_core__DOT__lo_a0;
        vlSelfRef.eg_a1 = vlSelfRef.u_core__DOT__lo_a1;
        vlSelfRef.eg_a2 = vlSelfRef.u_core__DOT__lo_a2;
        vlSelfRef.eg_dat = vlSelfRef.u_core__DOT__lo_dat;
    } else {
        vlSelfRef.eg_op = vlSelfRef.u_core__DOT__lx_op;
        vlSelfRef.eg_src = vlSelfRef.u_core__DOT__lx_src;
        vlSelfRef.eg_dst = vlSelfRef.u_core__DOT__lx_dst;
        vlSelfRef.eg_a0 = vlSelfRef.u_core__DOT__lx_a0;
        vlSelfRef.eg_a1 = vlSelfRef.u_core__DOT__lx_a1;
        vlSelfRef.eg_a2 = vlSelfRef.u_core__DOT__lx_a2;
        vlSelfRef.eg_dat = vlSelfRef.u_core__DOT__lx_dat;
    }
    vlSelfRef.u_core__DOT__u_rq__DOT__i_sel = vlSelfRef.u_core__DOT__hb_sel;
    vlSelfRef.u_core__DOT__u_rq__DOT__esel = 0U;
    if ((1U & (IData)(vlSelfRef.u_core__DOT__hb_sel))) {
        vlSelfRef.u_core__DOT__u_rq__DOT__esel = 0U;
    }
    if ((2U & (IData)(vlSelfRef.u_core__DOT__hb_sel))) {
        vlSelfRef.u_core__DOT__u_rq__DOT__esel = 1U;
    }
    if ((4U & (IData)(vlSelfRef.u_core__DOT__hb_sel))) {
        vlSelfRef.u_core__DOT__u_rq__DOT__esel = 2U;
    }
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__i_sel 
        = (1U & ((IData)(vlSelfRef.u_core__DOT__hb_sel) 
                 >> 0U));
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__i_sel 
        = (1U & ((IData)(vlSelfRef.u_core__DOT__hb_sel) 
                 >> 1U));
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__i_sel 
        = (1U & ((IData)(vlSelfRef.u_core__DOT__hb_sel) 
                 >> 2U));
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__i_sel 
        = (1U & ((IData)(vlSelfRef.u_core__DOT__hb_sel) 
                 >> 3U));
    vlSelfRef.hb_sel = vlSelfRef.u_core__DOT__hb_sel;
    vlSelfRef.u_core__DOT__u_rq__DOT__rsel = 0U;
    if ((1U & (IData)(vlSelfRef.u_core__DOT__hb_sel))) {
        vlSelfRef.u_core__DOT__u_rq__DOT__rsel = vlSelfRef.u_core__DOT__u_rq__DOT__R
            [0U];
    }
    if ((2U & (IData)(vlSelfRef.u_core__DOT__hb_sel))) {
        vlSelfRef.u_core__DOT__u_rq__DOT__rsel = vlSelfRef.u_core__DOT__u_rq__DOT__R
            [1U];
    }
    if ((4U & (IData)(vlSelfRef.u_core__DOT__hb_sel))) {
        vlSelfRef.u_core__DOT__u_rq__DOT__rsel = vlSelfRef.u_core__DOT__u_rq__DOT__R
            [2U];
    }
    if ((8U & (IData)(vlSelfRef.u_core__DOT__hb_sel))) {
        vlSelfRef.u_core__DOT__u_rq__DOT__esel = 3U;
        vlSelfRef.u_core__DOT__u_rq__DOT__rsel = vlSelfRef.u_core__DOT__u_rq__DOT__R
            [3U];
    }
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__wfin 
        = (0x1ffffU & ((IData)(vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__base) 
                       + (IData)(vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__eng)));
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__ival 
        = ((0U == vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__ivr)
            ? 1U : vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__ivr);
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__wfin 
        = (0x1ffffU & ((IData)(vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__base) 
                       + (IData)(vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__eng)));
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__ival 
        = ((0U == vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__ivr)
            ? 1U : vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__ivr);
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__wfin 
        = (0x1ffffU & ((IData)(vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__base) 
                       + (IData)(vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__eng)));
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__ival 
        = ((0U == vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__ivr)
            ? 1U : vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__ivr);
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__wfin 
        = (0x1ffffU & ((IData)(vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__base) 
                       + (IData)(vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__eng)));
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__ival 
        = ((0U == vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__ivr)
            ? 1U : vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__ivr);
    vlSelfRef.u_df__DOT__i_rd = vlSelfRef.df_rd;
    vlSelfRef.u_core__DOT__u_eg__DOT__i_tick = vlSelfRef.u_core__DOT__eg_tick;
    vlSelfRef.u_df__DOT__i_wr = vlSelfRef.df_wr_g;
    vlSelfRef.u_inbuf__DOT__m_ready = vlSelfRef.ci_ready_w;
    vlSelfRef.u_df__DOT__i_addr = vlSelfRef.df_addr_g;
    vlSelfRef.u_df__DOT__i_wdata = vlSelfRef.df_wdata_g;
    vlSelfRef.u_core__DOT__leak_sum = (0xfffffffffULL 
                                       & (vlSelfRef.u_core__DOT__act_e 
                                          - VL_SHIFTRS_QQI(36,36,4, vlSelfRef.u_core__DOT__act_e, (IData)(vlSelfRef.d_ka))));
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__i_base 
        = vlSelfRef.hb_base;
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__i_base 
        = vlSelfRef.hb_base;
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__i_base 
        = vlSelfRef.hb_base;
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__i_base 
        = vlSelfRef.hb_base;
    vlSelfRef.u_core__DOT__u_rq__DOT__i_tick = vlSelfRef.u_core__DOT__rq_tick;
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__i_cmd 
        = vlSelfRef.hb_cmd;
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__i_cmd 
        = vlSelfRef.hb_cmd;
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__i_cmd 
        = vlSelfRef.hb_cmd;
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__i_cmd 
        = vlSelfRef.hb_cmd;
    vlSelfRef.u_core__DOT__u_rq__DOT__i_train = vlSelfRef.u_core__DOT__rq_train;
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__i_gclass 
        = vlSelfRef.hb_gcl;
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__i_gclass 
        = vlSelfRef.hb_gcl;
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__i_gclass 
        = vlSelfRef.hb_gcl;
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__i_gclass 
        = vlSelfRef.hb_gcl;
    vlSelfRef.u_core__DOT__u_rq__DOT__gcl = vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__gcl;
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__gcl 
        = vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__gcl;
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__gcl 
        = vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__gcl;
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__gcl 
        = vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__gcl;
    vlSelfRef.u_core__DOT__u_rq__DOT__dsh = (0x3fU 
                                             & (((IData)(8U) 
                                                 + (IData)(vlSelfRef.d_qdw)) 
                                                - (IData)(vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__gcl)));
    vlSelfRef.u_core__DOT__lo_ready = vlSelfRef.lo_grant;
    vlSelfRef.u_core__DOT__lx_ready = vlSelfRef.lx_grant;
    vlSelfRef.u_egbuf__DOT__s_valid = vlSelfRef.eg_s_valid;
    vlSelfRef.u_egbuf__DOT__push = ((IData)(vlSelfRef.u_egbuf__DOT__s_ready) 
                                    & (IData)(vlSelfRef.eg_s_valid));
    vlSelfRef.u_egbuf__DOT__s_op = vlSelfRef.eg_op;
    vlSelfRef.u_egbuf__DOT__s_src = vlSelfRef.eg_src;
    vlSelfRef.u_egbuf__DOT__s_dst = vlSelfRef.eg_dst;
    vlSelfRef.u_egbuf__DOT__s_a0 = vlSelfRef.eg_a0;
    vlSelfRef.u_egbuf__DOT__s_a1 = vlSelfRef.eg_a1;
    vlSelfRef.u_egbuf__DOT__s_a2 = vlSelfRef.eg_a2;
    vlSelfRef.u_egbuf__DOT__s_dat = vlSelfRef.eg_dat;
    vlSelfRef.u_egbuf__DOT__s_bus[0U] = (IData)((((QData)((IData)(vlSelfRef.eg_a0)) 
                                                  << 0x30U) 
                                                 | (((QData)((IData)(
                                                                     (((IData)(vlSelfRef.eg_a1) 
                                                                       << 0x10U) 
                                                                      | (IData)(vlSelfRef.eg_a2)))) 
                                                     << 0x10U) 
                                                    | (QData)((IData)(vlSelfRef.eg_dat)))));
    vlSelfRef.u_egbuf__DOT__s_bus[1U] = (IData)(((((QData)((IData)(vlSelfRef.eg_a0)) 
                                                   << 0x30U) 
                                                  | (((QData)((IData)(
                                                                      (((IData)(vlSelfRef.eg_a1) 
                                                                        << 0x10U) 
                                                                       | (IData)(vlSelfRef.eg_a2)))) 
                                                      << 0x10U) 
                                                     | (QData)((IData)(vlSelfRef.eg_dat)))) 
                                                 >> 0x20U));
    vlSelfRef.u_egbuf__DOT__s_bus[2U] = (((IData)(vlSelfRef.eg_op) 
                                          << 8U) | 
                                         (((IData)(vlSelfRef.eg_src) 
                                           << 4U) | (IData)(vlSelfRef.eg_dst)));
    vlSelfRef.hb_w_mux = 0U;
    if ((1U & (IData)(vlSelfRef.hb_sel))) {
        vlSelfRef.hb_w_mux = (0xffffU & (IData)(vlSelfRef.w_flat));
    }
    if ((2U & (IData)(vlSelfRef.hb_sel))) {
        vlSelfRef.hb_w_mux = (0xffffU & (IData)((vlSelfRef.w_flat 
                                                 >> 0x10U)));
    }
    if ((4U & (IData)(vlSelfRef.hb_sel))) {
        vlSelfRef.hb_w_mux = (0xffffU & (IData)((vlSelfRef.w_flat 
                                                 >> 0x20U)));
    }
    if ((8U & (IData)(vlSelfRef.hb_sel))) {
        vlSelfRef.hb_w_mux = (0xffffU & (IData)((vlSelfRef.w_flat 
                                                 >> 0x30U)));
    }
    vlSelfRef.u_core__DOT__u_rq__DOT__rleak = (0xffffU 
                                               & ((IData)(vlSelfRef.u_core__DOT__u_rq__DOT__rsel) 
                                                  - 
                                                  ((IData)(vlSelfRef.u_core__DOT__u_rq__DOT__rsel) 
                                                   >> (IData)(vlSelfRef.d_qleak))));
    vlSelfRef.u_core__DOT__u_rq__DOT__cred_cur = ((IData)(vlSelfRef.u_core__DOT__u_rq__DOT__rsel) 
                                                  >> (IData)(vlSelfRef.d_qdw));
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__wout 
        = ((0x10000U & vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__wfin)
            ? 0xffffU : (0xffffU & vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__wfin));
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__decn 
        = ((0U != (IData)(vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__wh)) 
           & (vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__agen 
              >= vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__ival));
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__wout 
        = ((0x10000U & vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__wfin)
            ? 0xffffU : (0xffffU & vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__wfin));
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__decn 
        = ((0U != (IData)(vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__wh)) 
           & (vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__agen 
              >= vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__ival));
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__wout 
        = ((0x10000U & vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__wfin)
            ? 0xffffU : (0xffffU & vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__wfin));
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__decn 
        = ((0U != (IData)(vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__wh)) 
           & (vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__agen 
              >= vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__ival));
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__wout 
        = ((0x10000U & vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__wfin)
            ? 0xffffU : (0xffffU & vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__wfin));
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__decn 
        = ((0U != (IData)(vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__wh)) 
           & (vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__agen 
              >= vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__ival));
    vlSelfRef.u_core__DOT__u_rq__DOT__qbase = VL_SHIFTL_III(32,32,6, (IData)(1U), (IData)(vlSelfRef.u_core__DOT__u_rq__DOT__dsh));
    vlSelfRef.hb_w = vlSelfRef.hb_w_mux;
    vlSelfRef.u_core__DOT__u_rq__DOT__rsnap = ((1U 
                                                >= (IData)(vlSelfRef.u_core__DOT__u_rq__DOT__rleak)) 
                                               | ((IData)(vlSelfRef.u_core__DOT__u_rq__DOT__rleak) 
                                                  >= (IData)(vlSelfRef.u_core__DOT__u_rq__DOT__rsel)));
    vlSelfRef.u_core__DOT__rq_credit = ((IData)(vlSelfRef.d_rqen)
                                         ? (0xffffU 
                                            & vlSelfRef.u_core__DOT__u_rq__DOT__cred_cur)
                                         : 0U);
    vlSelfRef.u_core__DOT__u_rq__DOT__dep = (VL_SHIFTR_III(32,32,32, vlSelfRef.u_core__DOT__u_rq__DOT__qbase, 2U) 
                                             + VL_SHIFTR_III(32,32,32, vlSelfRef.u_core__DOT__u_rq__DOT__qbase, 5U));
    vlSelfRef.u_core__DOT__hb_w = vlSelfRef.hb_w;
    vlSelfRef.u_core__DOT__u_rq__DOT__rleakn = ((IData)(vlSelfRef.u_core__DOT__u_rq__DOT__rsnap)
                                                 ? 0U
                                                 : (IData)(vlSelfRef.u_core__DOT__u_rq__DOT__rleak));
    vlSelfRef.u_core__DOT__u_rq__DOT__o_credit = vlSelfRef.u_core__DOT__rq_credit;
    vlSelfRef.u_core__DOT__w_rq = (0x1ffffU & ((IData)(vlSelfRef.hb_w_mux) 
                                               + (IData)(vlSelfRef.u_core__DOT__rq_credit)));
    vlSelfRef.u_core__DOT__u_rq__DOT__rsum = (0x1ffffffffULL 
                                              & ((QData)((IData)(vlSelfRef.u_core__DOT__u_rq__DOT__rsel)) 
                                                 + (QData)((IData)(vlSelfRef.u_core__DOT__u_rq__DOT__dep))));
    vlSelfRef.u_core__DOT__hb_wq = ((0x10000U & vlSelfRef.u_core__DOT__w_rq)
                                     ? 0xffffU : (0xffffU 
                                                  & vlSelfRef.u_core__DOT__w_rq));
    vlSelfRef.u_core__DOT__u_rq__DOT__rsat = (vlSelfRef.u_core__DOT__u_rq__DOT__rsum 
                                              > vlSelfRef.u_core__DOT__u_rq__DOT__rfull);
    vlSelfRef.u_core__DOT__prod = (0x1ffffffffULL & 
                                   VL_MULS_QQQ(33, 
                                               (0x1ffffffffULL 
                                                & VL_EXTENDS_QI(33,17, (IData)(vlSelfRef.u_core__DOT__hb_wq))), 
                                               (0x1ffffffffULL 
                                                & VL_EXTENDS_QI(33,16, (IData)(vlSelfRef.u_core__DOT__lr_dat)))));
    vlSelfRef.u_core__DOT__u_rq__DOT__rdepn = ((IData)(vlSelfRef.u_core__DOT__u_rq__DOT__rsat)
                                                ? 0xffffU
                                                : (0xffffU 
                                                   & (IData)(vlSelfRef.u_core__DOT__u_rq__DOT__rsum)));
    vlSelfRef.u_core__DOT__prod_e = (((QData)((IData)(
                                                      (7U 
                                                       & (- (IData)(
                                                                    (1U 
                                                                     & (IData)(
                                                                               (vlSelfRef.u_core__DOT__prod 
                                                                                >> 0x20U)))))))) 
                                      << 0x21U) | vlSelfRef.u_core__DOT__prod);
    vlSelfRef.u_core__DOT__u_rq__DOT__cred_new = ((IData)(vlSelfRef.u_core__DOT__u_rq__DOT__rdepn) 
                                                  >> (IData)(vlSelfRef.d_qdw));
    vlSelfRef.u_core__DOT__eff_sum = (0xfffffffffULL 
                                      & (vlSelfRef.u_core__DOT__act_e 
                                         + VL_SHIFTRS_QQI(36,36,32, vlSelfRef.u_core__DOT__prod_e, 0xfU)));
    vlSelfRef.u_core__DOT__u_rq__DOT__o_antic = ((IData)(vlSelfRef.d_rqen) 
                                                 & ((IData)(vlSelfRef.u_core__DOT__rq_train) 
                                                    & (vlSelfRef.u_core__DOT__u_rq__DOT__cred_new 
                                                       > vlSelfRef.u_core__DOT__u_rq__DOT__cred_cur)));
    vlSelfRef.u_core__DOT__o_antic = vlSelfRef.u_core__DOT__u_rq__DOT__o_antic;
    vlSelfRef.w_antic = vlSelfRef.u_core__DOT__u_rq__DOT__o_antic;
}

VL_INLINE_OPT void Vq_fabric_top_q_cell___ico_sequent__TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell__0(Vq_fabric_top_q_cell* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    Vq_fabric_top__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vq_fabric_top_q_cell___ico_sequent__TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell__0\n"); );
    auto &vlSelfRef = std::ref(*vlSelf).get();
    // Init
    CData/*3:0*/ __Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__38__Vfuncout;
    __Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__38__Vfuncout = 0;
    SData/*15:0*/ __Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__38__v;
    __Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__38__v = 0;
    CData/*3:0*/ __Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__39__Vfuncout;
    __Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__39__Vfuncout = 0;
    SData/*15:0*/ __Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__39__v;
    __Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__39__v = 0;
    CData/*3:0*/ __Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__40__Vfuncout;
    __Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__40__Vfuncout = 0;
    SData/*15:0*/ __Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__40__v;
    __Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__40__v = 0;
    CData/*3:0*/ __Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__41__Vfuncout;
    __Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__41__Vfuncout = 0;
    SData/*15:0*/ __Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__41__v;
    __Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__41__v = 0;
    // Body
    vlSelfRef.u_core__DOT__u_eg__DOT__i_fire = vlSelfRef.u_core__DOT__eg_fire;
    vlSelfRef.u_core__DOT__u_rq__DOT__i_sel = vlSelfRef.u_core__DOT__hb_sel;
    vlSelfRef.u_core__DOT__u_rq__DOT__i_gclass = vlSelfRef.u_core__DOT__hb_gcl;
    vlSelfRef.u_core__DOT__u_rq__DOT__esel = 0U;
    if ((1U & (IData)(vlSelfRef.u_core__DOT__hb_sel))) {
        vlSelfRef.u_core__DOT__u_rq__DOT__esel = 0U;
    }
    if ((2U & (IData)(vlSelfRef.u_core__DOT__hb_sel))) {
        vlSelfRef.u_core__DOT__u_rq__DOT__esel = 1U;
    }
    if ((4U & (IData)(vlSelfRef.u_core__DOT__hb_sel))) {
        vlSelfRef.u_core__DOT__u_rq__DOT__esel = 2U;
    }
    vlSelfRef.u_rp__DOT__i_myid = vlSelfRef.i_myid;
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__i_sel 
        = (1U & ((IData)(vlSelfRef.u_core__DOT__hb_sel) 
                 >> 0U));
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__i_sel 
        = (1U & ((IData)(vlSelfRef.u_core__DOT__hb_sel) 
                 >> 1U));
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__i_sel 
        = (1U & ((IData)(vlSelfRef.u_core__DOT__hb_sel) 
                 >> 2U));
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__i_sel 
        = (1U & ((IData)(vlSelfRef.u_core__DOT__hb_sel) 
                 >> 3U));
    vlSelfRef.df_wr = vlSelfRef.u_core__DOT__df_wr;
    vlSelfRef.df_addr = vlSelfRef.u_core__DOT__df_addr;
    vlSelfRef.df_wdata = vlSelfRef.u_core__DOT__df_wdata;
    vlSelfRef.u_egbuf__DOT__m_valid = vlSelfRef.u_egbuf__DOT__a_v;
    vlSelfRef.w_act = vlSelfRef.u_core__DOT__act;
    vlSelfRef.u_core__DOT__o_ftrace = vlSelfRef.u_core__DOT__u_eg__DOT__f;
    vlSelfRef.u_core__DOT__u_eg__DOT__o_f = vlSelfRef.u_core__DOT__u_eg__DOT__f;
    vlSelfRef.u_df__DOT__o_eta_f = vlSelfRef.u_df__DOT__dial
        [0U];
    vlSelfRef.d_eta_f = vlSelfRef.u_df__DOT__dial[0U];
    vlSelfRef.u_df__DOT__o_eta_s = vlSelfRef.u_df__DOT__dial
        [1U];
    vlSelfRef.d_eta_s = vlSelfRef.u_df__DOT__dial[1U];
    vlSelfRef.u_df__DOT__o_thresh = vlSelfRef.u_df__DOT__dial
        [5U];
    vlSelfRef.u_df__DOT__o_refr = vlSelfRef.u_df__DOT__dial
        [6U];
    vlSelfRef.u_df__DOT__o_cosmin = vlSelfRef.u_df__DOT__dial
        [7U];
    vlSelfRef.d_cosmin = vlSelfRef.u_df__DOT__dial[7U];
    vlSelfRef.u_df__DOT__o_hl = vlSelfRef.u_df__DOT__dial
        [0xaU];
    vlSelfRef.u_df__DOT__o_floor = vlSelfRef.u_df__DOT__dial
        [0xcU];
    vlSelfRef.lo_valid = vlSelfRef.u_core__DOT__lo_valid;
    vlSelfRef.lx_valid = vlSelfRef.u_core__DOT__lx_valid;
    vlSelfRef.lo_op = vlSelfRef.u_core__DOT__lo_op;
    vlSelfRef.lx_op = vlSelfRef.u_core__DOT__lx_op;
    vlSelfRef.lo_src = vlSelfRef.u_core__DOT__lo_src;
    vlSelfRef.lx_src = vlSelfRef.u_core__DOT__lx_src;
    vlSelfRef.lo_dst = vlSelfRef.u_core__DOT__lo_dst;
    vlSelfRef.lx_dst = vlSelfRef.u_core__DOT__lx_dst;
    vlSelfRef.lo_a0 = vlSelfRef.u_core__DOT__lo_a0;
    vlSelfRef.lx_a0 = vlSelfRef.u_core__DOT__lx_a0;
    vlSelfRef.lo_a1 = vlSelfRef.u_core__DOT__lo_a1;
    vlSelfRef.lx_a1 = vlSelfRef.u_core__DOT__lx_a1;
    vlSelfRef.lo_a2 = vlSelfRef.u_core__DOT__lo_a2;
    vlSelfRef.lx_a2 = vlSelfRef.u_core__DOT__lx_a2;
    vlSelfRef.lo_dat = vlSelfRef.u_core__DOT__lo_dat;
    vlSelfRef.lx_dat = vlSelfRef.u_core__DOT__lx_dat;
    vlSelfRef.u_core__DOT__ci_a0_rsvd = (vlSelfRef.u_inbuf__DOT__a_q[1U] 
                                         >> 0x14U);
    vlSelfRef.u_inbuf__DOT__m_valid = vlSelfRef.u_inbuf__DOT__a_v;
    vlSelfRef.w_bound = vlSelfRef.u_core__DOT__bound;
    vlSelfRef.w_cid = vlSelfRef.u_core__DOT__cell_id;
    vlSelfRef.u_core__DOT__eff_pe = (((QData)((IData)(
                                                      (7U 
                                                       & (- (IData)(
                                                                    (1U 
                                                                     & (IData)(
                                                                               (vlSelfRef.u_core__DOT__eff_p 
                                                                                >> 0x20U)))))))) 
                                      << 0x21U) | vlSelfRef.u_core__DOT__eff_p);
    vlSelfRef.u_core__DOT__prod_p = (0x1ffffffffULL 
                                     & VL_MULS_QQQ(33, 
                                                   (0x1ffffffffULL 
                                                    & VL_EXTENDS_QI(33,17, (IData)(vlSelfRef.u_core__DOT__eff_w))), 
                                                   (0x1ffffffffULL 
                                                    & VL_EXTENDS_QI(33,16, (IData)(vlSelfRef.u_core__DOT__lr_dat)))));
    vlSelfRef.u_inbuf__DOT__pop = ((IData)(vlSelfRef.u_core__DOT__ci_ready) 
                                   & (IData)(vlSelfRef.u_inbuf__DOT__a_v));
    vlSelfRef.li_valid_w = vlSelfRef.u_egbuf__DOT__a_v;
    vlSelfRef.d_thresh = vlSelfRef.u_df__DOT__dial[5U];
    vlSelfRef.d_refr = vlSelfRef.u_df__DOT__dial[6U];
    vlSelfRef.w_ftrace = vlSelfRef.u_core__DOT__u_eg__DOT__f;
    vlSelfRef.u_core__DOT__rq_tick = (2U == (IData)(vlSelfRef.u_core__DOT__hb_cmd));
    vlSelfRef.u_df__DOT__o_kf = (0xfU & vlSelfRef.u_df__DOT__dial
                                 [2U]);
    vlSelfRef.u_df__DOT__o_ks = (0xfU & vlSelfRef.u_df__DOT__dial
                                 [3U]);
    vlSelfRef.u_inbuf__DOT__m_dst = (0xfU & vlSelfRef.u_inbuf__DOT__a_q[2U]);
    vlSelfRef.ci_valid = vlSelfRef.u_inbuf__DOT__a_v;
    vlSelfRef.ci_ready_w = vlSelfRef.u_core__DOT__ci_ready;
    vlSelfRef.df_rd = vlSelfRef.u_core__DOT__df_rd;
    vlSelfRef.df_rdata = vlSelfRef.u_df__DOT__o_rdata;
    vlSelfRef.df_rstb = vlSelfRef.u_df__DOT__o_rstb;
    vlSelfRef.u_core__DOT__eg_tick = (0x11U == (IData)(vlSelfRef.u_core__DOT__state));
    vlSelfRef.df_wr_g = ((IData)(vlSelfRef.i_bdf_wr) 
                         | (IData)(vlSelfRef.u_core__DOT__df_wr));
    vlSelfRef.u_core__DOT__eg_live = ((0U == vlSelfRef.u_df__DOT__dial
                                       [0xcU]) | ((IData)(vlSelfRef.u_core__DOT__u_eg__DOT__f) 
                                                  >= 
                                                  vlSelfRef.u_df__DOT__dial
                                                  [0xcU]));
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__hlc 
        = (0x1ffffU & ((IData)(1U) + (IData)(vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__hl_cnt)));
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__hlc 
        = (0x1ffffU & ((IData)(1U) + (IData)(vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__hl_cnt)));
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__hlc 
        = (0x1ffffU & ((IData)(1U) + (IData)(vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__hl_cnt)));
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__hlc 
        = (0x1ffffU & ((IData)(1U) + (IData)(vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__hl_cnt)));
    if (vlSelfRef.i_bdf_wr) {
        vlSelfRef.df_addr_g = vlSelfRef.i_bdf_addr;
        vlSelfRef.df_wdata_g = vlSelfRef.i_bdf_wdata;
    } else {
        vlSelfRef.df_addr_g = vlSelfRef.u_core__DOT__df_addr;
        vlSelfRef.df_wdata_g = vlSelfRef.u_core__DOT__df_wdata;
    }
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__agen 
        = ((IData)(1U) + vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__age);
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__agen 
        = ((IData)(1U) + vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__age);
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__agen 
        = ((IData)(1U) + vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__age);
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__agen 
        = ((IData)(1U) + vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__age);
    vlSelfRef.ci_op = (7U & (vlSelfRef.u_inbuf__DOT__a_q[2U] 
                             >> 8U));
    vlSelfRef.ci_src = (0xfU & (vlSelfRef.u_inbuf__DOT__a_q[2U] 
                                >> 4U));
    vlSelfRef.ci_a0 = (vlSelfRef.u_inbuf__DOT__a_q[1U] 
                       >> 0x10U);
    vlSelfRef.ci_a1 = (0xffffU & vlSelfRef.u_inbuf__DOT__a_q[1U]);
    vlSelfRef.ci_a2 = (vlSelfRef.u_inbuf__DOT__a_q[0U] 
                       >> 0x10U);
    vlSelfRef.ci_dat = (0xffffU & vlSelfRef.u_inbuf__DOT__a_q[0U]);
    vlSelfRef.u_core__DOT__act_e = (((QData)((IData)(
                                                     (0xfffffU 
                                                      & (- (IData)(
                                                                   (1U 
                                                                    & ((IData)(vlSelfRef.u_core__DOT__act) 
                                                                       >> 0xfU))))))) 
                                     << 0x10U) | (QData)((IData)(vlSelfRef.u_core__DOT__act)));
    vlSelfRef.eg_s_valid = ((IData)(vlSelfRef.u_core__DOT__lo_valid) 
                            | (IData)(vlSelfRef.u_core__DOT__lx_valid));
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__ridx32 
        = vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__ridx;
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__ridx32 
        = vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__ridx;
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__ridx32 
        = vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__ridx;
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__ridx32 
        = vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__ridx;
    vlSelfRef.done_vec = (((IData)(vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__o_done) 
                           << 3U) | (((IData)(vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__o_done) 
                                      << 2U) | (((IData)(vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__o_done) 
                                                 << 1U) 
                                                | (IData)(vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__o_done))));
    vlSelfRef.d_ka = (0xfU & vlSelfRef.u_df__DOT__dial
                      [4U]);
    vlSelfRef.hb_cmd = vlSelfRef.u_core__DOT__hb_cmd;
    vlSelfRef.hb_gcl = vlSelfRef.u_core__DOT__hb_gcl;
    vlSelfRef.d_hl = vlSelfRef.u_df__DOT__dial[0xaU];
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__whs 
        = ((0xffU < (IData)(vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__wh))
            ? 0xffffU : (0xffffU & VL_SHIFTL_III(16,16,32, (IData)(vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__wh), 8U)));
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__whs 
        = ((0xffU < (IData)(vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__wh))
            ? 0xffffU : (0xffffU & VL_SHIFTL_III(16,16,32, (IData)(vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__wh), 8U)));
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__whs 
        = ((0xffU < (IData)(vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__wh))
            ? 0xffffU : (0xffffU & VL_SHIFTL_III(16,16,32, (IData)(vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__wh), 8U)));
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__whs 
        = ((0xffU < (IData)(vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__wh))
            ? 0xffffU : (0xffffU & VL_SHIFTL_III(16,16,32, (IData)(vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__wh), 8U)));
    vlSelfRef.hb_base = vlSelfRef.u_core__DOT__hb_base;
    if (vlSelfRef.u_core__DOT__lo_valid) {
        vlSelfRef.eg_op = vlSelfRef.u_core__DOT__lo_op;
        vlSelfRef.eg_src = vlSelfRef.u_core__DOT__lo_src;
        vlSelfRef.eg_dst = vlSelfRef.u_core__DOT__lo_dst;
        vlSelfRef.eg_a0 = vlSelfRef.u_core__DOT__lo_a0;
        vlSelfRef.eg_a1 = vlSelfRef.u_core__DOT__lo_a1;
        vlSelfRef.eg_a2 = vlSelfRef.u_core__DOT__lo_a2;
        vlSelfRef.eg_dat = vlSelfRef.u_core__DOT__lo_dat;
    } else {
        vlSelfRef.eg_op = vlSelfRef.u_core__DOT__lx_op;
        vlSelfRef.eg_src = vlSelfRef.u_core__DOT__lx_src;
        vlSelfRef.eg_dst = vlSelfRef.u_core__DOT__lx_dst;
        vlSelfRef.eg_a0 = vlSelfRef.u_core__DOT__lx_a0;
        vlSelfRef.eg_a1 = vlSelfRef.u_core__DOT__lx_a1;
        vlSelfRef.eg_a2 = vlSelfRef.u_core__DOT__lx_a2;
        vlSelfRef.eg_dat = vlSelfRef.u_core__DOT__lx_dat;
    }
    vlSelfRef.u_core__DOT__rq_train = (5U == (IData)(vlSelfRef.u_core__DOT__hb_cmd));
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__g_lad_sat__DOT__sat 
        = (1U & (vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__acc 
                 >> 0x10U));
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__g_lad_sat__DOT__sat 
        = (1U & (vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__acc 
                 >> 0x10U));
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__g_lad_sat__DOT__sat 
        = (1U & (vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__acc 
                 >> 0x10U));
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__g_lad_sat__DOT__sat 
        = (1U & (vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__acc 
                 >> 0x10U));
    vlSelfRef.d_kle = (0xfU & vlSelfRef.u_df__DOT__dial
                       [0xbU]);
    __Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__38__v 
        = vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__wh;
    __Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__38__Vfuncout = 0U;
    if ((1U & (IData)(__Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__38__v))) {
        __Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__38__Vfuncout = 0U;
    }
    if ((2U & (IData)(__Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__38__v))) {
        __Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__38__Vfuncout = 1U;
    }
    if ((4U & (IData)(__Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__38__v))) {
        __Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__38__Vfuncout = 2U;
    }
    if ((8U & (IData)(__Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__38__v))) {
        __Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__38__Vfuncout = 3U;
    }
    if ((0x10U & (IData)(__Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__38__v))) {
        __Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__38__Vfuncout = 4U;
    }
    if ((0x20U & (IData)(__Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__38__v))) {
        __Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__38__Vfuncout = 5U;
    }
    if ((0x40U & (IData)(__Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__38__v))) {
        __Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__38__Vfuncout = 6U;
    }
    if ((0x80U & (IData)(__Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__38__v))) {
        __Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__38__Vfuncout = 7U;
    }
    if ((0x100U & (IData)(__Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__38__v))) {
        __Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__38__Vfuncout = 8U;
    }
    if ((0x200U & (IData)(__Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__38__v))) {
        __Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__38__Vfuncout = 9U;
    }
    if ((0x400U & (IData)(__Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__38__v))) {
        __Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__38__Vfuncout = 0xaU;
    }
    if ((0x800U & (IData)(__Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__38__v))) {
        __Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__38__Vfuncout = 0xbU;
    }
    if ((0x1000U & (IData)(__Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__38__v))) {
        __Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__38__Vfuncout = 0xcU;
    }
    if ((0x2000U & (IData)(__Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__38__v))) {
        __Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__38__Vfuncout = 0xdU;
    }
    if ((0x4000U & (IData)(__Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__38__v))) {
        __Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__38__Vfuncout = 0xeU;
    }
    if ((0x8000U & (IData)(__Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__38__v))) {
        __Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__38__Vfuncout = 0xfU;
    }
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__wmsb 
        = __Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__38__Vfuncout;
    __Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__39__v 
        = vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__wh;
    __Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__39__Vfuncout = 0U;
    if ((1U & (IData)(__Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__39__v))) {
        __Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__39__Vfuncout = 0U;
    }
    if ((2U & (IData)(__Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__39__v))) {
        __Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__39__Vfuncout = 1U;
    }
    if ((4U & (IData)(__Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__39__v))) {
        __Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__39__Vfuncout = 2U;
    }
    if ((8U & (IData)(__Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__39__v))) {
        __Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__39__Vfuncout = 3U;
    }
    if ((0x10U & (IData)(__Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__39__v))) {
        __Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__39__Vfuncout = 4U;
    }
    if ((0x20U & (IData)(__Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__39__v))) {
        __Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__39__Vfuncout = 5U;
    }
    if ((0x40U & (IData)(__Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__39__v))) {
        __Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__39__Vfuncout = 6U;
    }
    if ((0x80U & (IData)(__Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__39__v))) {
        __Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__39__Vfuncout = 7U;
    }
    if ((0x100U & (IData)(__Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__39__v))) {
        __Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__39__Vfuncout = 8U;
    }
    if ((0x200U & (IData)(__Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__39__v))) {
        __Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__39__Vfuncout = 9U;
    }
    if ((0x400U & (IData)(__Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__39__v))) {
        __Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__39__Vfuncout = 0xaU;
    }
    if ((0x800U & (IData)(__Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__39__v))) {
        __Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__39__Vfuncout = 0xbU;
    }
    if ((0x1000U & (IData)(__Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__39__v))) {
        __Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__39__Vfuncout = 0xcU;
    }
    if ((0x2000U & (IData)(__Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__39__v))) {
        __Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__39__Vfuncout = 0xdU;
    }
    if ((0x4000U & (IData)(__Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__39__v))) {
        __Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__39__Vfuncout = 0xeU;
    }
    if ((0x8000U & (IData)(__Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__39__v))) {
        __Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__39__Vfuncout = 0xfU;
    }
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__wmsb 
        = __Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__39__Vfuncout;
    __Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__40__v 
        = vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__wh;
    __Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__40__Vfuncout = 0U;
    if ((1U & (IData)(__Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__40__v))) {
        __Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__40__Vfuncout = 0U;
    }
    if ((2U & (IData)(__Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__40__v))) {
        __Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__40__Vfuncout = 1U;
    }
    if ((4U & (IData)(__Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__40__v))) {
        __Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__40__Vfuncout = 2U;
    }
    if ((8U & (IData)(__Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__40__v))) {
        __Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__40__Vfuncout = 3U;
    }
    if ((0x10U & (IData)(__Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__40__v))) {
        __Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__40__Vfuncout = 4U;
    }
    if ((0x20U & (IData)(__Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__40__v))) {
        __Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__40__Vfuncout = 5U;
    }
    if ((0x40U & (IData)(__Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__40__v))) {
        __Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__40__Vfuncout = 6U;
    }
    if ((0x80U & (IData)(__Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__40__v))) {
        __Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__40__Vfuncout = 7U;
    }
    if ((0x100U & (IData)(__Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__40__v))) {
        __Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__40__Vfuncout = 8U;
    }
    if ((0x200U & (IData)(__Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__40__v))) {
        __Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__40__Vfuncout = 9U;
    }
    if ((0x400U & (IData)(__Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__40__v))) {
        __Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__40__Vfuncout = 0xaU;
    }
    if ((0x800U & (IData)(__Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__40__v))) {
        __Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__40__Vfuncout = 0xbU;
    }
    if ((0x1000U & (IData)(__Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__40__v))) {
        __Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__40__Vfuncout = 0xcU;
    }
    if ((0x2000U & (IData)(__Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__40__v))) {
        __Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__40__Vfuncout = 0xdU;
    }
    if ((0x4000U & (IData)(__Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__40__v))) {
        __Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__40__Vfuncout = 0xeU;
    }
    if ((0x8000U & (IData)(__Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__40__v))) {
        __Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__40__Vfuncout = 0xfU;
    }
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__wmsb 
        = __Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__40__Vfuncout;
    __Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__41__v 
        = vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__wh;
    __Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__41__Vfuncout = 0U;
    if ((1U & (IData)(__Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__41__v))) {
        __Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__41__Vfuncout = 0U;
    }
    if ((2U & (IData)(__Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__41__v))) {
        __Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__41__Vfuncout = 1U;
    }
    if ((4U & (IData)(__Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__41__v))) {
        __Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__41__Vfuncout = 2U;
    }
    if ((8U & (IData)(__Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__41__v))) {
        __Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__41__Vfuncout = 3U;
    }
    if ((0x10U & (IData)(__Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__41__v))) {
        __Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__41__Vfuncout = 4U;
    }
    if ((0x20U & (IData)(__Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__41__v))) {
        __Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__41__Vfuncout = 5U;
    }
    if ((0x40U & (IData)(__Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__41__v))) {
        __Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__41__Vfuncout = 6U;
    }
    if ((0x80U & (IData)(__Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__41__v))) {
        __Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__41__Vfuncout = 7U;
    }
    if ((0x100U & (IData)(__Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__41__v))) {
        __Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__41__Vfuncout = 8U;
    }
    if ((0x200U & (IData)(__Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__41__v))) {
        __Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__41__Vfuncout = 9U;
    }
    if ((0x400U & (IData)(__Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__41__v))) {
        __Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__41__Vfuncout = 0xaU;
    }
    if ((0x800U & (IData)(__Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__41__v))) {
        __Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__41__Vfuncout = 0xbU;
    }
    if ((0x1000U & (IData)(__Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__41__v))) {
        __Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__41__Vfuncout = 0xcU;
    }
    if ((0x2000U & (IData)(__Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__41__v))) {
        __Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__41__Vfuncout = 0xdU;
    }
    if ((0x4000U & (IData)(__Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__41__v))) {
        __Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__41__Vfuncout = 0xeU;
    }
    if ((0x8000U & (IData)(__Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__41__v))) {
        __Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__41__Vfuncout = 0xfU;
    }
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__wmsb 
        = __Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__41__Vfuncout;
    vlSelfRef.d_floor = vlSelfRef.u_df__DOT__dial[0xcU];
    vlSelfRef.u_egbuf__DOT__s_ready = (1U & (~ (IData)(vlSelfRef.u_egbuf__DOT__b_v)));
    vlSelfRef.d_qleak = (0xfU & vlSelfRef.u_df__DOT__dial
                         [0xfU]);
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__hlth 
        = vlSelfRef.u_df__DOT__dial[0xaU];
    vlSelfRef.hb_sel = vlSelfRef.u_core__DOT__hb_sel;
    vlSelfRef.ovf_vec = (((IData)(vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__o_ovf) 
                          << 3U) | (((IData)(vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__o_ovf) 
                                     << 2U) | (((IData)(vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__o_ovf) 
                                                << 1U) 
                                               | (IData)(vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__o_ovf))));
    vlSelfRef.w_flat = (((QData)((IData)(vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__o_w)) 
                         << 0x30U) | (((QData)((IData)(
                                                       (((IData)(vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__o_w) 
                                                         << 0x10U) 
                                                        | (IData)(vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__o_w)))) 
                                       << 0x10U) | (QData)((IData)(vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__o_w))));
    vlSelfRef.li_op_w = (7U & (vlSelfRef.u_egbuf__DOT__a_q[2U] 
                               >> 8U));
    vlSelfRef.li_src_w = (0xfU & (vlSelfRef.u_egbuf__DOT__a_q[2U] 
                                  >> 4U));
    vlSelfRef.li_dst_w = (0xfU & vlSelfRef.u_egbuf__DOT__a_q[2U]);
    vlSelfRef.li_a0_w = (vlSelfRef.u_egbuf__DOT__a_q[1U] 
                         >> 0x10U);
    vlSelfRef.li_a1_w = (0xffffU & vlSelfRef.u_egbuf__DOT__a_q[1U]);
    vlSelfRef.li_a2_w = (vlSelfRef.u_egbuf__DOT__a_q[0U] 
                         >> 0x10U);
    vlSelfRef.li_dat_w = (0xffffU & vlSelfRef.u_egbuf__DOT__a_q[0U]);
    vlSelfRef.d_rqen = (1U & (vlSelfRef.u_df__DOT__dial
                              [0xeU] >> 0xfU));
    vlSelfRef.d_mode = (1U & vlSelfRef.u_df__DOT__dial
                        [9U]);
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__gcl 
        = ((8U <= (IData)(vlSelfRef.u_core__DOT__hb_gcl))
            ? 7U : (IData)(vlSelfRef.u_core__DOT__hb_gcl));
    vlSelfRef.d_p0e = (0x1fU & vlSelfRef.u_df__DOT__dial
                       [8U]);
    vlSelfRef.u_core__DOT__u_rq__DOT__rsel = 0U;
    if ((1U & (IData)(vlSelfRef.u_core__DOT__hb_sel))) {
        vlSelfRef.u_core__DOT__u_rq__DOT__rsel = vlSelfRef.u_core__DOT__u_rq__DOT__R
            [0U];
    }
    if ((2U & (IData)(vlSelfRef.u_core__DOT__hb_sel))) {
        vlSelfRef.u_core__DOT__u_rq__DOT__rsel = vlSelfRef.u_core__DOT__u_rq__DOT__R
            [1U];
    }
    if ((4U & (IData)(vlSelfRef.u_core__DOT__hb_sel))) {
        vlSelfRef.u_core__DOT__u_rq__DOT__rsel = vlSelfRef.u_core__DOT__u_rq__DOT__R
            [2U];
    }
    if ((8U & (IData)(vlSelfRef.u_core__DOT__hb_sel))) {
        vlSelfRef.u_core__DOT__u_rq__DOT__esel = 3U;
        vlSelfRef.u_core__DOT__u_rq__DOT__rsel = vlSelfRef.u_core__DOT__u_rq__DOT__R
            [3U];
    }
    vlSelfRef.d_qdw = (0xfU & vlSelfRef.u_df__DOT__dial
                       [0xeU]);
    vlSelfRef.ld_ready = (1U & (~ (IData)(vlSelfRef.u_inbuf__DOT__b_v)));
    vlSelfRef.u_df__DOT__rst_n = vlSelfRef.i_por_n;
    vlSelfRef.u_inbuf__DOT__rst_n = vlSelfRef.rst_n;
    vlSelfRef.u_egbuf__DOT__rst_n = vlSelfRef.rst_n;
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__rst_n 
        = vlSelfRef.rst_n;
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__rst_n 
        = vlSelfRef.rst_n;
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__rst_n 
        = vlSelfRef.rst_n;
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__rst_n 
        = vlSelfRef.rst_n;
    vlSelfRef.u_core__DOT__rst_n = vlSelfRef.rst_n;
    vlSelfRef.u_df__DOT__clk = vlSelfRef.clk;
    vlSelfRef.u_inbuf__DOT__clk = vlSelfRef.clk;
    vlSelfRef.u_egbuf__DOT__clk = vlSelfRef.clk;
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__clk 
        = vlSelfRef.clk;
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__clk 
        = vlSelfRef.clk;
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__clk 
        = vlSelfRef.clk;
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__clk 
        = vlSelfRef.clk;
    vlSelfRef.u_core__DOT__clk = vlSelfRef.clk;
    vlSelfRef.u_rp__DOT__ri_valid = vlSelfRef.ri_valid;
    vlSelfRef.u_rp__DOT__ro_ready = vlSelfRef.ro_ready;
    vlSelfRef.u_rp__DOT__ri_op = vlSelfRef.ri_op;
    vlSelfRef.u_rp__DOT__ld_op = vlSelfRef.ri_op;
    vlSelfRef.ld_op = vlSelfRef.ri_op;
    vlSelfRef.u_rp__DOT__ri_src = vlSelfRef.ri_src;
    vlSelfRef.u_rp__DOT__ld_src = vlSelfRef.ri_src;
    vlSelfRef.ld_src = vlSelfRef.ri_src;
    vlSelfRef.u_rp__DOT__ri_a0 = vlSelfRef.ri_a0;
    vlSelfRef.u_rp__DOT__ld_a0 = vlSelfRef.ri_a0;
    vlSelfRef.ld_a0 = vlSelfRef.ri_a0;
    vlSelfRef.u_rp__DOT__ri_a1 = vlSelfRef.ri_a1;
    vlSelfRef.u_rp__DOT__ld_a1 = vlSelfRef.ri_a1;
    vlSelfRef.ld_a1 = vlSelfRef.ri_a1;
    vlSelfRef.u_rp__DOT__ri_a2 = vlSelfRef.ri_a2;
    vlSelfRef.u_rp__DOT__ld_a2 = vlSelfRef.ri_a2;
    vlSelfRef.ld_a2 = vlSelfRef.ri_a2;
    vlSelfRef.u_rp__DOT__ri_dat = vlSelfRef.ri_dat;
    vlSelfRef.u_rp__DOT__ld_dat = vlSelfRef.ri_dat;
    vlSelfRef.ld_dat = vlSelfRef.ri_dat;
    vlSelfRef.u_core__DOT__s_tick = vlSelfRef.s_tick;
    vlSelfRef.u_rp__DOT__ri_dst = vlSelfRef.ri_dst;
    vlSelfRef.u_rp__DOT__ld_dst = vlSelfRef.ri_dst;
    vlSelfRef.w_lddst = vlSelfRef.ri_dst;
    vlSelfRef.u_inbuf__DOT__s_bus[0U] = (IData)((((QData)((IData)(vlSelfRef.ri_a0)) 
                                                  << 0x30U) 
                                                 | (((QData)((IData)(
                                                                     (((IData)(vlSelfRef.ri_a1) 
                                                                       << 0x10U) 
                                                                      | (IData)(vlSelfRef.ri_a2)))) 
                                                     << 0x10U) 
                                                    | (QData)((IData)(vlSelfRef.ri_dat)))));
    vlSelfRef.u_inbuf__DOT__s_bus[1U] = (IData)(((((QData)((IData)(vlSelfRef.ri_a0)) 
                                                   << 0x30U) 
                                                  | (((QData)((IData)(
                                                                      (((IData)(vlSelfRef.ri_a1) 
                                                                        << 0x10U) 
                                                                       | (IData)(vlSelfRef.ri_a2)))) 
                                                      << 0x10U) 
                                                     | (QData)((IData)(vlSelfRef.ri_dat)))) 
                                                 >> 0x20U));
    vlSelfRef.u_inbuf__DOT__s_bus[2U] = (((IData)(vlSelfRef.ri_op) 
                                          << 8U) | 
                                         (((IData)(vlSelfRef.ri_src) 
                                           << 4U) | (IData)(vlSelfRef.ri_dst)));
    vlSelfRef.ld_valid = ((IData)(vlSelfRef.ri_valid) 
                          & ((IData)(vlSelfRef.i_myid) 
                             == (IData)(vlSelfRef.ri_dst)));
    vlSelfRef.u_rp__DOT__li_valid = vlSelfRef.li_valid_w;
    vlSelfRef.u_core__DOT__d_thresh = vlSelfRef.d_thresh;
    vlSelfRef.u_core__DOT__d_refr = vlSelfRef.d_refr;
    vlSelfRef.u_df__DOT__i_probe = vlSelfRef.w_ftrace;
    vlSelfRef.u_core__DOT__u_rq__DOT__i_tick = vlSelfRef.u_core__DOT__rq_tick;
    vlSelfRef.d_kf = vlSelfRef.u_df__DOT__o_kf;
    vlSelfRef.d_ks = vlSelfRef.u_df__DOT__o_ks;
    vlSelfRef.w_indst = vlSelfRef.u_inbuf__DOT__m_dst;
    vlSelfRef.u_core__DOT__ci_valid = vlSelfRef.ci_valid;
    vlSelfRef.u_inbuf__DOT__m_ready = vlSelfRef.ci_ready_w;
    vlSelfRef.u_df__DOT__i_rd = vlSelfRef.df_rd;
    vlSelfRef.u_core__DOT__df_rdata = vlSelfRef.df_rdata;
    vlSelfRef.u_core__DOT__df_rstb = vlSelfRef.df_rstb;
    vlSelfRef.u_core__DOT__u_eg__DOT__i_tick = vlSelfRef.u_core__DOT__eg_tick;
    vlSelfRef.u_df__DOT__i_wr = vlSelfRef.df_wr_g;
    vlSelfRef.u_core__DOT__u_eg__DOT__o_live = vlSelfRef.u_core__DOT__eg_live;
    vlSelfRef.u_df__DOT__i_addr = vlSelfRef.df_addr_g;
    vlSelfRef.u_df__DOT__i_wdata = vlSelfRef.df_wdata_g;
    vlSelfRef.u_core__DOT__ci_op = vlSelfRef.ci_op;
    vlSelfRef.u_inbuf__DOT__m_op = vlSelfRef.ci_op;
    vlSelfRef.u_core__DOT__ci_src = vlSelfRef.ci_src;
    vlSelfRef.u_inbuf__DOT__m_src = vlSelfRef.ci_src;
    vlSelfRef.u_core__DOT__ci_a0 = vlSelfRef.ci_a0;
    vlSelfRef.u_inbuf__DOT__m_a0 = vlSelfRef.ci_a0;
    vlSelfRef.u_core__DOT__ci_a1 = vlSelfRef.ci_a1;
    vlSelfRef.u_inbuf__DOT__m_a1 = vlSelfRef.ci_a1;
    vlSelfRef.u_core__DOT__ci_a2 = vlSelfRef.ci_a2;
    vlSelfRef.u_inbuf__DOT__m_a2 = vlSelfRef.ci_a2;
    vlSelfRef.u_core__DOT__ci_dat = vlSelfRef.ci_dat;
    vlSelfRef.u_inbuf__DOT__m_dat = vlSelfRef.ci_dat;
    vlSelfRef.u_egbuf__DOT__s_valid = vlSelfRef.eg_s_valid;
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__rsh 
        = ((IData)(8U) - vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__ridx32);
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__rsh 
        = ((IData)(8U) - vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__ridx32);
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__rsh 
        = ((IData)(8U) - vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__ridx32);
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__rsh 
        = ((IData)(8U) - vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__ridx32);
    vlSelfRef.hb_done = (0U != (IData)(vlSelfRef.done_vec));
    vlSelfRef.u_core__DOT__d_ka = vlSelfRef.d_ka;
    vlSelfRef.u_df__DOT__o_ka = vlSelfRef.d_ka;
    vlSelfRef.u_core__DOT__leak_sum = (0xfffffffffULL 
                                       & (vlSelfRef.u_core__DOT__act_e 
                                          - VL_SHIFTRS_QQI(36,36,4, vlSelfRef.u_core__DOT__act_e, (IData)(vlSelfRef.d_ka))));
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__i_cmd 
        = vlSelfRef.hb_cmd;
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__i_cmd 
        = vlSelfRef.hb_cmd;
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__i_cmd 
        = vlSelfRef.hb_cmd;
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__i_cmd 
        = vlSelfRef.hb_cmd;
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__i_gclass 
        = vlSelfRef.hb_gcl;
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__i_gclass 
        = vlSelfRef.hb_gcl;
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__i_gclass 
        = vlSelfRef.hb_gcl;
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__i_gclass 
        = vlSelfRef.hb_gcl;
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__i_hl 
        = vlSelfRef.d_hl;
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__i_hl 
        = vlSelfRef.d_hl;
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__i_hl 
        = vlSelfRef.d_hl;
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__i_hl 
        = vlSelfRef.d_hl;
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__i_base 
        = vlSelfRef.hb_base;
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__i_base 
        = vlSelfRef.hb_base;
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__i_base 
        = vlSelfRef.hb_base;
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__i_base 
        = vlSelfRef.hb_base;
    vlSelfRef.u_egbuf__DOT__s_op = vlSelfRef.eg_op;
    vlSelfRef.u_egbuf__DOT__s_src = vlSelfRef.eg_src;
    vlSelfRef.u_egbuf__DOT__s_dst = vlSelfRef.eg_dst;
    vlSelfRef.u_egbuf__DOT__s_a0 = vlSelfRef.eg_a0;
    vlSelfRef.u_egbuf__DOT__s_a1 = vlSelfRef.eg_a1;
    vlSelfRef.u_egbuf__DOT__s_a2 = vlSelfRef.eg_a2;
    vlSelfRef.u_egbuf__DOT__s_dat = vlSelfRef.eg_dat;
    vlSelfRef.u_egbuf__DOT__s_bus[0U] = (IData)((((QData)((IData)(vlSelfRef.eg_a0)) 
                                                  << 0x30U) 
                                                 | (((QData)((IData)(
                                                                     (((IData)(vlSelfRef.eg_a1) 
                                                                       << 0x10U) 
                                                                      | (IData)(vlSelfRef.eg_a2)))) 
                                                     << 0x10U) 
                                                    | (QData)((IData)(vlSelfRef.eg_dat)))));
    vlSelfRef.u_egbuf__DOT__s_bus[1U] = (IData)(((((QData)((IData)(vlSelfRef.eg_a0)) 
                                                   << 0x30U) 
                                                  | (((QData)((IData)(
                                                                      (((IData)(vlSelfRef.eg_a1) 
                                                                        << 0x10U) 
                                                                       | (IData)(vlSelfRef.eg_a2)))) 
                                                      << 0x10U) 
                                                     | (QData)((IData)(vlSelfRef.eg_dat)))) 
                                                 >> 0x20U));
    vlSelfRef.u_egbuf__DOT__s_bus[2U] = (((IData)(vlSelfRef.eg_op) 
                                          << 8U) | 
                                         (((IData)(vlSelfRef.eg_src) 
                                           << 4U) | (IData)(vlSelfRef.eg_dst)));
    vlSelfRef.u_core__DOT__u_rq__DOT__i_train = vlSelfRef.u_core__DOT__rq_train;
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__lad 
        = ((IData)(vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__g_lad_sat__DOT__sat)
            ? 0xffffU : (0xffffU & vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__acc));
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__lad 
        = ((IData)(vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__g_lad_sat__DOT__sat)
            ? 0xffffU : (0xffffU & vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__acc));
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__lad 
        = ((IData)(vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__g_lad_sat__DOT__sat)
            ? 0xffffU : (0xffffU & vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__acc));
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__lad 
        = ((IData)(vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__g_lad_sat__DOT__sat)
            ? 0xffffU : (0xffffU & vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__acc));
    vlSelfRef.u_df__DOT__o_kle = vlSelfRef.d_kle;
    vlSelfRef.u_core__DOT__d_kle = vlSelfRef.d_kle;
    vlSelfRef.u_core__DOT__u_eg__DOT__fleak = (0xffffU 
                                               & ((IData)(vlSelfRef.u_core__DOT__u_eg__DOT__f) 
                                                  - 
                                                  ((IData)(vlSelfRef.u_core__DOT__u_eg__DOT__f) 
                                                   >> (IData)(vlSelfRef.d_kle))));
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__shl2 
        = (0x1fU & ((IData)(vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__wmsb) 
                    + (IData)(vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__wmsb)));
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__shl2 
        = (0x1fU & ((IData)(vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__wmsb) 
                    + (IData)(vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__wmsb)));
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__shl2 
        = (0x1fU & ((IData)(vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__wmsb) 
                    + (IData)(vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__wmsb)));
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__shl2 
        = (0x1fU & ((IData)(vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__wmsb) 
                    + (IData)(vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__wmsb)));
    vlSelfRef.u_core__DOT__d_floor = vlSelfRef.d_floor;
    vlSelfRef.u_core__DOT__u_eg__DOT__o_gclass = ((
                                                   (0U 
                                                    == (IData)(vlSelfRef.d_floor)) 
                                                   | (0U 
                                                      == (IData)(vlSelfRef.u_core__DOT__u_eg__DOT__f)))
                                                   ? 0U
                                                   : 
                                                  (0xfU 
                                                   & ((IData)(0xfU) 
                                                      - 
                                                      ([&]() {
                        vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__37__v 
                            = vlSelfRef.u_core__DOT__u_eg__DOT__f;
                        vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__37__Vfuncout = 0U;
                        if ((1U & (IData)(vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__37__v))) {
                            vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__37__Vfuncout = 0U;
                        }
                        vlSelfRef.u_core__DOT__u_eg__DOT__msb_idx__Vstatic__j = 1U;
                        if ((2U & (IData)(vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__37__v))) {
                            vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__37__Vfuncout = 1U;
                        }
                        vlSelfRef.u_core__DOT__u_eg__DOT__msb_idx__Vstatic__j = 2U;
                        if ((4U & (IData)(vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__37__v))) {
                            vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__37__Vfuncout = 2U;
                        }
                        vlSelfRef.u_core__DOT__u_eg__DOT__msb_idx__Vstatic__j = 3U;
                        if ((8U & (IData)(vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__37__v))) {
                            vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__37__Vfuncout = 3U;
                        }
                        vlSelfRef.u_core__DOT__u_eg__DOT__msb_idx__Vstatic__j = 4U;
                        if ((0x10U & (IData)(vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__37__v))) {
                            vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__37__Vfuncout = 4U;
                        }
                        vlSelfRef.u_core__DOT__u_eg__DOT__msb_idx__Vstatic__j = 5U;
                        if ((0x20U & (IData)(vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__37__v))) {
                            vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__37__Vfuncout = 5U;
                        }
                        vlSelfRef.u_core__DOT__u_eg__DOT__msb_idx__Vstatic__j = 6U;
                        if ((0x40U & (IData)(vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__37__v))) {
                            vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__37__Vfuncout = 6U;
                        }
                        vlSelfRef.u_core__DOT__u_eg__DOT__msb_idx__Vstatic__j = 7U;
                        if ((0x80U & (IData)(vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__37__v))) {
                            vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__37__Vfuncout = 7U;
                        }
                        vlSelfRef.u_core__DOT__u_eg__DOT__msb_idx__Vstatic__j = 8U;
                        if ((0x100U & (IData)(vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__37__v))) {
                            vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__37__Vfuncout = 8U;
                        }
                        vlSelfRef.u_core__DOT__u_eg__DOT__msb_idx__Vstatic__j = 9U;
                        if ((0x200U & (IData)(vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__37__v))) {
                            vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__37__Vfuncout = 9U;
                        }
                        vlSelfRef.u_core__DOT__u_eg__DOT__msb_idx__Vstatic__j = 0xaU;
                        if ((0x400U & (IData)(vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__37__v))) {
                            vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__37__Vfuncout = 0xaU;
                        }
                        vlSelfRef.u_core__DOT__u_eg__DOT__msb_idx__Vstatic__j = 0xbU;
                        if ((0x800U & (IData)(vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__37__v))) {
                            vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__37__Vfuncout = 0xbU;
                        }
                        vlSelfRef.u_core__DOT__u_eg__DOT__msb_idx__Vstatic__j = 0xcU;
                        if ((0x1000U & (IData)(vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__37__v))) {
                            vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__37__Vfuncout = 0xcU;
                        }
                        vlSelfRef.u_core__DOT__u_eg__DOT__msb_idx__Vstatic__j = 0xdU;
                        if ((0x2000U & (IData)(vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__37__v))) {
                            vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__37__Vfuncout = 0xdU;
                        }
                        vlSelfRef.u_core__DOT__u_eg__DOT__msb_idx__Vstatic__j = 0xeU;
                        if ((0x4000U & (IData)(vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__37__v))) {
                            vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__37__Vfuncout = 0xeU;
                        }
                        vlSelfRef.u_core__DOT__u_eg__DOT__msb_idx__Vstatic__j = 0xfU;
                        if ((0x8000U & (IData)(vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__37__v))) {
                            vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__37__Vfuncout = 0xfU;
                        }
                        vlSelfRef.u_core__DOT__u_eg__DOT__msb_idx__Vstatic__j = 0x10U;
                    }(), (IData)(vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__37__Vfuncout)))));
    vlSelfRef.eg_s_ready = vlSelfRef.u_egbuf__DOT__s_ready;
    vlSelfRef.u_egbuf__DOT__push = ((IData)(vlSelfRef.u_egbuf__DOT__s_ready) 
                                    & (IData)(vlSelfRef.eg_s_valid));
    vlSelfRef.lo_grant = (1U & ((~ (IData)(vlSelfRef.u_core__DOT__lo_valid)) 
                                | (IData)(vlSelfRef.u_egbuf__DOT__s_ready)));
    vlSelfRef.lx_grant = ((~ (IData)(vlSelfRef.u_core__DOT__lo_valid)) 
                          & (IData)(vlSelfRef.u_egbuf__DOT__s_ready));
    vlSelfRef.u_df__DOT__o_qleak = vlSelfRef.d_qleak;
    vlSelfRef.u_core__DOT__d_qleak = vlSelfRef.d_qleak;
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__hlth 
        = vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__hlth;
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__hlth 
        = vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__hlth;
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__hlth 
        = vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__hlth;
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__hlend 
        = (vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__hlc 
           >= vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__hlth);
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__hlend 
        = (vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__hlc 
           >= vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__hlth);
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__hlend 
        = (vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__hlc 
           >= vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__hlth);
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__hlend 
        = (vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__hlc 
           >= vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__hlth);
    vlSelfRef.o_ovf = (0U != (IData)(vlSelfRef.ovf_vec));
    vlSelfRef.hb_w_mux = 0U;
    if ((1U & (IData)(vlSelfRef.hb_sel))) {
        vlSelfRef.hb_w_mux = (0xffffU & (IData)(vlSelfRef.w_flat));
    }
    if ((2U & (IData)(vlSelfRef.hb_sel))) {
        vlSelfRef.hb_w_mux = (0xffffU & (IData)((vlSelfRef.w_flat 
                                                 >> 0x10U)));
    }
    if ((4U & (IData)(vlSelfRef.hb_sel))) {
        vlSelfRef.hb_w_mux = (0xffffU & (IData)((vlSelfRef.w_flat 
                                                 >> 0x20U)));
    }
    if ((8U & (IData)(vlSelfRef.hb_sel))) {
        vlSelfRef.hb_w_mux = (0xffffU & (IData)((vlSelfRef.w_flat 
                                                 >> 0x30U)));
    }
    vlSelfRef.u_rp__DOT__li_op = vlSelfRef.li_op_w;
    vlSelfRef.u_egbuf__DOT__m_op = vlSelfRef.li_op_w;
    vlSelfRef.u_rp__DOT__li_src = vlSelfRef.li_src_w;
    vlSelfRef.u_egbuf__DOT__m_src = vlSelfRef.li_src_w;
    vlSelfRef.u_rp__DOT__li_dst = vlSelfRef.li_dst_w;
    vlSelfRef.u_egbuf__DOT__m_dst = vlSelfRef.li_dst_w;
    vlSelfRef.u_rp__DOT__li_a0 = vlSelfRef.li_a0_w;
    vlSelfRef.u_egbuf__DOT__m_a0 = vlSelfRef.li_a0_w;
    vlSelfRef.u_rp__DOT__li_a1 = vlSelfRef.li_a1_w;
    vlSelfRef.u_egbuf__DOT__m_a1 = vlSelfRef.li_a1_w;
    vlSelfRef.u_rp__DOT__li_a2 = vlSelfRef.li_a2_w;
    vlSelfRef.u_egbuf__DOT__m_a2 = vlSelfRef.li_a2_w;
    vlSelfRef.u_rp__DOT__li_dat = vlSelfRef.li_dat_w;
    vlSelfRef.u_egbuf__DOT__m_dat = vlSelfRef.li_dat_w;
    vlSelfRef.u_df__DOT__o_rqen = vlSelfRef.d_rqen;
    vlSelfRef.u_core__DOT__d_rqen = vlSelfRef.d_rqen;
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__i_mode 
        = vlSelfRef.d_mode;
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__i_mode 
        = vlSelfRef.d_mode;
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__i_mode 
        = vlSelfRef.d_mode;
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__i_mode 
        = vlSelfRef.d_mode;
    vlSelfRef.u_df__DOT__o_mode = vlSelfRef.d_mode;
    vlSelfRef.u_core__DOT__u_rq__DOT__gcl = vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__gcl;
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__gcl 
        = vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__gcl;
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__gcl 
        = vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__gcl;
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__gcl 
        = vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__gcl;
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__i_p0e 
        = vlSelfRef.d_p0e;
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__i_p0e 
        = vlSelfRef.d_p0e;
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__i_p0e 
        = vlSelfRef.d_p0e;
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__i_p0e 
        = vlSelfRef.d_p0e;
    vlSelfRef.u_df__DOT__o_p0e = vlSelfRef.d_p0e;
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__p0 
        = ((IData)(1U) << (IData)(vlSelfRef.d_p0e));
    vlSelfRef.u_core__DOT__u_rq__DOT__rleak = (0xffffU 
                                               & ((IData)(vlSelfRef.u_core__DOT__u_rq__DOT__rsel) 
                                                  - 
                                                  ((IData)(vlSelfRef.u_core__DOT__u_rq__DOT__rsel) 
                                                   >> (IData)(vlSelfRef.d_qleak))));
    vlSelfRef.u_df__DOT__o_qdw = vlSelfRef.d_qdw;
    vlSelfRef.u_core__DOT__d_qdw = vlSelfRef.d_qdw;
    vlSelfRef.u_core__DOT__u_rq__DOT__cred_cur = ((IData)(vlSelfRef.u_core__DOT__u_rq__DOT__rsel) 
                                                  >> (IData)(vlSelfRef.d_qdw));
    vlSelfRef.u_core__DOT__u_rq__DOT__dsh = (0x3fU 
                                             & (((IData)(8U) 
                                                 + (IData)(vlSelfRef.d_qdw)) 
                                                - (IData)(vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__gcl)));
    vlSelfRef.u_rp__DOT__ld_ready = vlSelfRef.ld_ready;
    vlSelfRef.u_inbuf__DOT__s_ready = vlSelfRef.ld_ready;
    vlSelfRef.u_core__DOT__u_eg__DOT__rst_n = vlSelfRef.u_core__DOT__rst_n;
    vlSelfRef.u_core__DOT__u_rq__DOT__rst_n = vlSelfRef.u_core__DOT__rst_n;
    vlSelfRef.u_core__DOT__u_eg__DOT__clk = vlSelfRef.u_core__DOT__clk;
    vlSelfRef.u_core__DOT__u_rq__DOT__clk = vlSelfRef.u_core__DOT__clk;
    vlSelfRef.u_inbuf__DOT__s_op = vlSelfRef.ld_op;
    vlSelfRef.u_inbuf__DOT__s_src = vlSelfRef.ld_src;
    vlSelfRef.u_inbuf__DOT__s_a0 = vlSelfRef.ld_a0;
    vlSelfRef.u_inbuf__DOT__s_a1 = vlSelfRef.ld_a1;
    vlSelfRef.u_inbuf__DOT__s_a2 = vlSelfRef.ld_a2;
    vlSelfRef.u_inbuf__DOT__s_dat = vlSelfRef.ld_dat;
    vlSelfRef.u_inbuf__DOT__s_dst = vlSelfRef.w_lddst;
    if (vlSelfRef.ld_valid) {
        vlSelfRef.u_inbuf__DOT__s_valid = 1U;
        vlSelfRef.u_rp__DOT__ld_valid = 1U;
        vlSelfRef.u_rp__DOT__hit = 1U;
        vlSelfRef.u_rp__DOT__ri_ready = vlSelfRef.ld_ready;
        vlSelfRef.u_inbuf__DOT__push = vlSelfRef.ld_ready;
    } else {
        vlSelfRef.u_inbuf__DOT__s_valid = 0U;
        vlSelfRef.u_rp__DOT__ld_valid = 0U;
        vlSelfRef.u_rp__DOT__hit = 0U;
        vlSelfRef.u_rp__DOT__ri_ready = vlSelfRef.ro_ready;
        vlSelfRef.u_inbuf__DOT__push = 0U;
    }
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__addw 
        = (0x1ffffU & VL_SHIFTL_III(17,17,32, vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__c
                                    [(7U & (IData)(vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__ridx))], vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__rsh));
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__addw 
        = (0x1ffffU & VL_SHIFTL_III(17,17,32, vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__c
                                    [(7U & (IData)(vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__ridx))], vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__rsh));
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__addw 
        = (0x1ffffU & VL_SHIFTL_III(17,17,32, vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__c
                                    [(7U & (IData)(vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__ridx))], vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__rsh));
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__addw 
        = (0x1ffffU & VL_SHIFTL_III(17,17,32, vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__c
                                    [(7U & (IData)(vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__ridx))], vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__rsh));
    vlSelfRef.u_core__DOT__hb_done = vlSelfRef.hb_done;
    if (vlSelfRef.d_mode) {
        vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__eng 
            = vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__whs;
        vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__eng 
            = vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__whs;
        vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__eng 
            = vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__whs;
        vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__eng 
            = vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__whs;
    } else {
        vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__eng 
            = vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__lad;
        vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__eng 
            = vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__lad;
        vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__eng 
            = vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__lad;
        vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__eng 
            = vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__lad;
    }
    vlSelfRef.u_core__DOT__u_eg__DOT__i_kle = vlSelfRef.u_core__DOT__d_kle;
    vlSelfRef.u_core__DOT__u_eg__DOT__fsnap = (((IData)(vlSelfRef.u_core__DOT__u_eg__DOT__fleak) 
                                                <= 
                                                vlSelfRef.u_df__DOT__dial
                                                [0xcU]) 
                                               | ((1U 
                                                   >= (IData)(vlSelfRef.u_core__DOT__u_eg__DOT__fleak)) 
                                                  | ((IData)(vlSelfRef.u_core__DOT__u_eg__DOT__fleak) 
                                                     >= (IData)(vlSelfRef.u_core__DOT__u_eg__DOT__f))));
    vlSelfRef.u_core__DOT__u_eg__DOT__i_floor = vlSelfRef.u_core__DOT__d_floor;
    vlSelfRef.u_core__DOT__eg_gclass = vlSelfRef.u_core__DOT__u_eg__DOT__o_gclass;
    vlSelfRef.u_core__DOT__lo_ready = vlSelfRef.lo_grant;
    vlSelfRef.u_core__DOT__lx_ready = vlSelfRef.lx_grant;
    vlSelfRef.u_core__DOT__u_rq__DOT__i_qleak = vlSelfRef.u_core__DOT__d_qleak;
    vlSelfRef.hb_w = vlSelfRef.hb_w_mux;
    vlSelfRef.u_core__DOT__u_rq__DOT__i_en = vlSelfRef.u_core__DOT__d_rqen;
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__p0 
        = vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__p0;
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__p0 
        = vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__p0;
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__p0 
        = vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__p0;
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__ivr 
        = (vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__p0 
           >> (IData)(vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__shl2));
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__ivr 
        = (vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__p0 
           >> (IData)(vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__shl2));
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__ivr 
        = (vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__p0 
           >> (IData)(vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__shl2));
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__ivr 
        = (vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__p0 
           >> (IData)(vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__shl2));
    vlSelfRef.u_core__DOT__u_rq__DOT__rsnap = ((1U 
                                                >= (IData)(vlSelfRef.u_core__DOT__u_rq__DOT__rleak)) 
                                               | ((IData)(vlSelfRef.u_core__DOT__u_rq__DOT__rleak) 
                                                  >= (IData)(vlSelfRef.u_core__DOT__u_rq__DOT__rsel)));
    vlSelfRef.u_core__DOT__u_rq__DOT__i_qdw = vlSelfRef.u_core__DOT__d_qdw;
    vlSelfRef.u_core__DOT__rq_credit = ((IData)(vlSelfRef.d_rqen)
                                         ? (0xffffU 
                                            & vlSelfRef.u_core__DOT__u_rq__DOT__cred_cur)
                                         : 0U);
    vlSelfRef.u_core__DOT__u_rq__DOT__qbase = VL_SHIFTL_III(32,32,6, (IData)(1U), (IData)(vlSelfRef.u_core__DOT__u_rq__DOT__dsh));
    vlSelfRef.ri_ready = vlSelfRef.u_rp__DOT__ri_ready;
    vlSelfRef.u_rp__DOT__consumed = vlSelfRef.u_inbuf__DOT__push;
    vlSelfRef.u_rp__DOT__inject_ok = (1U & ((~ (IData)(vlSelfRef.ri_valid)) 
                                            | (IData)(vlSelfRef.u_inbuf__DOT__push)));
    vlSelfRef.u_rp__DOT__transit = ((~ (IData)(vlSelfRef.u_inbuf__DOT__push)) 
                                    & (IData)(vlSelfRef.ri_valid));
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__wfin 
        = (0x1ffffU & ((IData)(vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__base) 
                       + (IData)(vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__eng)));
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__wfin 
        = (0x1ffffU & ((IData)(vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__base) 
                       + (IData)(vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__eng)));
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__wfin 
        = (0x1ffffU & ((IData)(vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__base) 
                       + (IData)(vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__eng)));
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__wfin 
        = (0x1ffffU & ((IData)(vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__base) 
                       + (IData)(vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__eng)));
    vlSelfRef.u_core__DOT__hb_w = vlSelfRef.hb_w;
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__ival 
        = ((0U == vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__ivr)
            ? 1U : vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__ivr);
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__ival 
        = ((0U == vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__ivr)
            ? 1U : vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__ivr);
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__ival 
        = ((0U == vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__ivr)
            ? 1U : vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__ivr);
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__ival 
        = ((0U == vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__ivr)
            ? 1U : vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__ivr);
    vlSelfRef.u_core__DOT__u_rq__DOT__rleakn = ((IData)(vlSelfRef.u_core__DOT__u_rq__DOT__rsnap)
                                                 ? 0U
                                                 : (IData)(vlSelfRef.u_core__DOT__u_rq__DOT__rleak));
    vlSelfRef.u_core__DOT__u_rq__DOT__o_credit = vlSelfRef.u_core__DOT__rq_credit;
    vlSelfRef.u_core__DOT__w_rq = (0x1ffffU & ((IData)(vlSelfRef.hb_w_mux) 
                                               + (IData)(vlSelfRef.u_core__DOT__rq_credit)));
    vlSelfRef.u_core__DOT__u_rq__DOT__dep = (VL_SHIFTR_III(32,32,32, vlSelfRef.u_core__DOT__u_rq__DOT__qbase, 2U) 
                                             + VL_SHIFTR_III(32,32,32, vlSelfRef.u_core__DOT__u_rq__DOT__qbase, 5U));
    vlSelfRef.li_ready_w = ((IData)(vlSelfRef.u_rp__DOT__inject_ok) 
                            & (IData)(vlSelfRef.ro_ready));
    vlSelfRef.u_rp__DOT__ro_valid = ((IData)(vlSelfRef.u_rp__DOT__transit) 
                                     | ((IData)(vlSelfRef.u_egbuf__DOT__a_v) 
                                        & (IData)(vlSelfRef.u_rp__DOT__inject_ok)));
    if (vlSelfRef.u_rp__DOT__transit) {
        vlSelfRef.u_rp__DOT__ro_op = vlSelfRef.ri_op;
        vlSelfRef.u_rp__DOT__ro_src = vlSelfRef.ri_src;
        vlSelfRef.u_rp__DOT__ro_dst = vlSelfRef.ri_dst;
        vlSelfRef.u_rp__DOT__ro_a0 = vlSelfRef.ri_a0;
        vlSelfRef.u_rp__DOT__ro_a1 = vlSelfRef.ri_a1;
        vlSelfRef.u_rp__DOT__ro_a2 = vlSelfRef.ri_a2;
        vlSelfRef.u_rp__DOT__ro_dat = vlSelfRef.ri_dat;
    } else {
        vlSelfRef.u_rp__DOT__ro_op = vlSelfRef.li_op_w;
        vlSelfRef.u_rp__DOT__ro_src = vlSelfRef.li_src_w;
        vlSelfRef.u_rp__DOT__ro_dst = vlSelfRef.li_dst_w;
        vlSelfRef.u_rp__DOT__ro_a0 = vlSelfRef.li_a0_w;
        vlSelfRef.u_rp__DOT__ro_a1 = vlSelfRef.li_a1_w;
        vlSelfRef.u_rp__DOT__ro_a2 = vlSelfRef.li_a2_w;
        vlSelfRef.u_rp__DOT__ro_dat = vlSelfRef.li_dat_w;
    }
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__wout 
        = ((0x10000U & vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__wfin)
            ? 0xffffU : (0xffffU & vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__wfin));
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__wout 
        = ((0x10000U & vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__wfin)
            ? 0xffffU : (0xffffU & vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__wfin));
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__wout 
        = ((0x10000U & vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__wfin)
            ? 0xffffU : (0xffffU & vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__wfin));
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__wout 
        = ((0x10000U & vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__wfin)
            ? 0xffffU : (0xffffU & vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__wfin));
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__decn 
        = ((0U != (IData)(vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__wh)) 
           & (vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__agen 
              >= vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__ival));
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__decn 
        = ((0U != (IData)(vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__wh)) 
           & (vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__agen 
              >= vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__ival));
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__decn 
        = ((0U != (IData)(vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__wh)) 
           & (vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__agen 
              >= vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__ival));
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__decn 
        = ((0U != (IData)(vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__wh)) 
           & (vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__agen 
              >= vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__ival));
    vlSelfRef.u_core__DOT__hb_wq = ((0x10000U & vlSelfRef.u_core__DOT__w_rq)
                                     ? 0xffffU : (0xffffU 
                                                  & vlSelfRef.u_core__DOT__w_rq));
    vlSelfRef.u_core__DOT__u_rq__DOT__rsum = (0x1ffffffffULL 
                                              & ((QData)((IData)(vlSelfRef.u_core__DOT__u_rq__DOT__rsel)) 
                                                 + (QData)((IData)(vlSelfRef.u_core__DOT__u_rq__DOT__dep))));
    vlSelfRef.u_egbuf__DOT__m_ready = vlSelfRef.li_ready_w;
    vlSelfRef.u_rp__DOT__li_ready = vlSelfRef.li_ready_w;
    vlSelfRef.u_egbuf__DOT__pop = ((IData)(vlSelfRef.u_egbuf__DOT__a_v) 
                                   & (IData)(vlSelfRef.li_ready_w));
    vlSelfRef.ro_valid = vlSelfRef.u_rp__DOT__ro_valid;
    vlSelfRef.ro_op = vlSelfRef.u_rp__DOT__ro_op;
    vlSelfRef.ro_src = vlSelfRef.u_rp__DOT__ro_src;
    vlSelfRef.ro_dst = vlSelfRef.u_rp__DOT__ro_dst;
    vlSelfRef.ro_a0 = vlSelfRef.u_rp__DOT__ro_a0;
    vlSelfRef.ro_a1 = vlSelfRef.u_rp__DOT__ro_a1;
    vlSelfRef.ro_a2 = vlSelfRef.u_rp__DOT__ro_a2;
    vlSelfRef.ro_dat = vlSelfRef.u_rp__DOT__ro_dat;
    vlSelfRef.u_core__DOT__prod = (0x1ffffffffULL & 
                                   VL_MULS_QQQ(33, 
                                               (0x1ffffffffULL 
                                                & VL_EXTENDS_QI(33,17, (IData)(vlSelfRef.u_core__DOT__hb_wq))), 
                                               (0x1ffffffffULL 
                                                & VL_EXTENDS_QI(33,16, (IData)(vlSelfRef.u_core__DOT__lr_dat)))));
    vlSelfRef.u_core__DOT__u_rq__DOT__rsat = (vlSelfRef.u_core__DOT__u_rq__DOT__rsum 
                                              > vlSelfRef.u_core__DOT__u_rq__DOT__rfull);
    vlSelfRef.u_core__DOT__prod_e = (((QData)((IData)(
                                                      (7U 
                                                       & (- (IData)(
                                                                    (1U 
                                                                     & (IData)(
                                                                               (vlSelfRef.u_core__DOT__prod 
                                                                                >> 0x20U)))))))) 
                                      << 0x21U) | vlSelfRef.u_core__DOT__prod);
    vlSelfRef.u_core__DOT__u_rq__DOT__rdepn = ((IData)(vlSelfRef.u_core__DOT__u_rq__DOT__rsat)
                                                ? 0xffffU
                                                : (0xffffU 
                                                   & (IData)(vlSelfRef.u_core__DOT__u_rq__DOT__rsum)));
    vlSelfRef.u_core__DOT__eff_sum = (0xfffffffffULL 
                                      & (vlSelfRef.u_core__DOT__act_e 
                                         + VL_SHIFTRS_QQI(36,36,32, vlSelfRef.u_core__DOT__prod_e, 0xfU)));
    vlSelfRef.u_core__DOT__u_rq__DOT__cred_new = ((IData)(vlSelfRef.u_core__DOT__u_rq__DOT__rdepn) 
                                                  >> (IData)(vlSelfRef.d_qdw));
    vlSelfRef.u_core__DOT__u_rq__DOT__o_antic = ((IData)(vlSelfRef.d_rqen) 
                                                 & ((IData)(vlSelfRef.u_core__DOT__rq_train) 
                                                    & (vlSelfRef.u_core__DOT__u_rq__DOT__cred_new 
                                                       > vlSelfRef.u_core__DOT__u_rq__DOT__cred_cur)));
    vlSelfRef.u_core__DOT__o_antic = vlSelfRef.u_core__DOT__u_rq__DOT__o_antic;
    vlSelfRef.w_antic = vlSelfRef.u_core__DOT__u_rq__DOT__o_antic;
}

VL_INLINE_OPT void Vq_fabric_top_q_cell___nba_sequent__TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell__0(Vq_fabric_top_q_cell* vlSelf) {
    (void)vlSelf;  // Prevent unused variable warning
    Vq_fabric_top__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    VL_DEBUG_IF(VL_DBG_MSGF("+        Vq_fabric_top_q_cell___nba_sequent__TOP__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell__0\n"); );
    auto &vlSelfRef = std::ref(*vlSelf).get();
    // Init
    SData/*15:0*/ __Vfunc_u_core__DOT__sclip16__35__Vfuncout;
    __Vfunc_u_core__DOT__sclip16__35__Vfuncout = 0;
    QData/*35:0*/ __Vfunc_u_core__DOT__sclip16__35__v;
    __Vfunc_u_core__DOT__sclip16__35__v = 0;
    SData/*15:0*/ __Vfunc_u_core__DOT__sclip16__36__Vfuncout;
    __Vfunc_u_core__DOT__sclip16__36__Vfuncout = 0;
    QData/*35:0*/ __Vfunc_u_core__DOT__sclip16__36__v;
    __Vfunc_u_core__DOT__sclip16__36__v = 0;
    CData/*3:0*/ __Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__38__Vfuncout;
    __Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__38__Vfuncout = 0;
    SData/*15:0*/ __Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__38__v;
    __Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__38__v = 0;
    CData/*3:0*/ __Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__39__Vfuncout;
    __Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__39__Vfuncout = 0;
    SData/*15:0*/ __Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__39__v;
    __Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__39__v = 0;
    CData/*3:0*/ __Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__40__Vfuncout;
    __Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__40__Vfuncout = 0;
    SData/*15:0*/ __Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__40__v;
    __Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__40__v = 0;
    CData/*3:0*/ __Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__41__Vfuncout;
    __Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__41__Vfuncout = 0;
    SData/*15:0*/ __Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__41__v;
    __Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__41__v = 0;
    CData/*0:0*/ __Vdly__u_core__DOT__lo_valid;
    __Vdly__u_core__DOT__lo_valid = 0;
    CData/*0:0*/ __Vdly__u_core__DOT__lx_valid;
    __Vdly__u_core__DOT__lx_valid = 0;
    CData/*4:0*/ __Vdly__u_core__DOT__state;
    __Vdly__u_core__DOT__state = 0;
    SData/*15:0*/ __Vdly__u_core__DOT__act;
    __Vdly__u_core__DOT__act = 0;
    CData/*0:0*/ __Vdly__u_core__DOT__ci_ready;
    __Vdly__u_core__DOT__ci_ready = 0;
    SData/*15:0*/ __Vdly__u_core__DOT__refr;
    __Vdly__u_core__DOT__refr = 0;
    CData/*2:0*/ __Vdly__u_core__DOT__eidx;
    __Vdly__u_core__DOT__eidx = 0;
    IData/*18:0*/ __Vdly__u_core__DOT__wacc;
    __Vdly__u_core__DOT__wacc = 0;
    CData/*0:0*/ __Vdly__u_core__DOT__tick_pend;
    __Vdly__u_core__DOT__tick_pend = 0;
    CData/*0:0*/ __Vdly__u_inbuf__DOT__a_v;
    __Vdly__u_inbuf__DOT__a_v = 0;
    CData/*0:0*/ __Vdly__u_egbuf__DOT__a_v;
    __Vdly__u_egbuf__DOT__a_v = 0;
    SData/*15:0*/ __Vdly__edges__BRA__0__KET____DOT__u_hebb__DOT__wh;
    __Vdly__edges__BRA__0__KET____DOT__u_hebb__DOT__wh = 0;
    IData/*23:0*/ __Vdly__edges__BRA__0__KET____DOT__u_hebb__DOT__age;
    __Vdly__edges__BRA__0__KET____DOT__u_hebb__DOT__age = 0;
    SData/*15:0*/ __Vdly__edges__BRA__0__KET____DOT__u_hebb__DOT__hl_cnt;
    __Vdly__edges__BRA__0__KET____DOT__u_hebb__DOT__hl_cnt = 0;
    SData/*15:0*/ __Vdly__edges__BRA__1__KET____DOT__u_hebb__DOT__wh;
    __Vdly__edges__BRA__1__KET____DOT__u_hebb__DOT__wh = 0;
    IData/*23:0*/ __Vdly__edges__BRA__1__KET____DOT__u_hebb__DOT__age;
    __Vdly__edges__BRA__1__KET____DOT__u_hebb__DOT__age = 0;
    SData/*15:0*/ __Vdly__edges__BRA__1__KET____DOT__u_hebb__DOT__hl_cnt;
    __Vdly__edges__BRA__1__KET____DOT__u_hebb__DOT__hl_cnt = 0;
    SData/*15:0*/ __Vdly__edges__BRA__2__KET____DOT__u_hebb__DOT__wh;
    __Vdly__edges__BRA__2__KET____DOT__u_hebb__DOT__wh = 0;
    IData/*23:0*/ __Vdly__edges__BRA__2__KET____DOT__u_hebb__DOT__age;
    __Vdly__edges__BRA__2__KET____DOT__u_hebb__DOT__age = 0;
    SData/*15:0*/ __Vdly__edges__BRA__2__KET____DOT__u_hebb__DOT__hl_cnt;
    __Vdly__edges__BRA__2__KET____DOT__u_hebb__DOT__hl_cnt = 0;
    SData/*15:0*/ __Vdly__edges__BRA__3__KET____DOT__u_hebb__DOT__wh;
    __Vdly__edges__BRA__3__KET____DOT__u_hebb__DOT__wh = 0;
    IData/*23:0*/ __Vdly__edges__BRA__3__KET____DOT__u_hebb__DOT__age;
    __Vdly__edges__BRA__3__KET____DOT__u_hebb__DOT__age = 0;
    SData/*15:0*/ __Vdly__edges__BRA__3__KET____DOT__u_hebb__DOT__hl_cnt;
    __Vdly__edges__BRA__3__KET____DOT__u_hebb__DOT__hl_cnt = 0;
    CData/*3:0*/ __VdlyVal__u_core__DOT__etab__v0;
    __VdlyVal__u_core__DOT__etab__v0 = 0;
    CData/*1:0*/ __VdlyDim0__u_core__DOT__etab__v0;
    __VdlyDim0__u_core__DOT__etab__v0 = 0;
    CData/*0:0*/ __VdlySet__u_core__DOT__etab__v0;
    __VdlySet__u_core__DOT__etab__v0 = 0;
    CData/*1:0*/ __VdlyDim0__u_core__DOT__ev__v0;
    __VdlyDim0__u_core__DOT__ev__v0 = 0;
    CData/*0:0*/ __VdlySet__u_core__DOT__etab__v1;
    __VdlySet__u_core__DOT__etab__v1 = 0;
    SData/*15:0*/ __VdlyVal__u_core__DOT__u_rq__DOT__R__v0;
    __VdlyVal__u_core__DOT__u_rq__DOT__R__v0 = 0;
    CData/*1:0*/ __VdlyDim0__u_core__DOT__u_rq__DOT__R__v0;
    __VdlyDim0__u_core__DOT__u_rq__DOT__R__v0 = 0;
    CData/*0:0*/ __VdlySet__u_core__DOT__u_rq__DOT__R__v0;
    __VdlySet__u_core__DOT__u_rq__DOT__R__v0 = 0;
    SData/*15:0*/ __VdlyVal__u_core__DOT__u_rq__DOT__R__v1;
    __VdlyVal__u_core__DOT__u_rq__DOT__R__v1 = 0;
    CData/*1:0*/ __VdlyDim0__u_core__DOT__u_rq__DOT__R__v1;
    __VdlyDim0__u_core__DOT__u_rq__DOT__R__v1 = 0;
    CData/*0:0*/ __VdlySet__u_core__DOT__u_rq__DOT__R__v1;
    __VdlySet__u_core__DOT__u_rq__DOT__R__v1 = 0;
    CData/*0:0*/ __VdlySet__u_core__DOT__u_rq__DOT__R__v2;
    __VdlySet__u_core__DOT__u_rq__DOT__R__v2 = 0;
    SData/*15:0*/ __VdlyVal__u_df__DOT__dial__v0;
    __VdlyVal__u_df__DOT__dial__v0 = 0;
    CData/*3:0*/ __VdlyDim0__u_df__DOT__dial__v0;
    __VdlyDim0__u_df__DOT__dial__v0 = 0;
    CData/*0:0*/ __VdlySet__u_df__DOT__dial__v0;
    __VdlySet__u_df__DOT__dial__v0 = 0;
    CData/*0:0*/ __VdlySet__u_df__DOT__dial__v1;
    __VdlySet__u_df__DOT__dial__v1 = 0;
    CData/*7:0*/ __VdlyVal__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v0;
    __VdlyVal__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v0 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v0;
    __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v0 = 0;
    CData/*7:0*/ __VdlyVal__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v1;
    __VdlyVal__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v1 = 0;
    CData/*2:0*/ __VdlyDim0__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v1;
    __VdlyDim0__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v1 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v1;
    __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v1 = 0;
    CData/*7:0*/ __VdlyVal__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v2;
    __VdlyVal__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v2 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v2;
    __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v2 = 0;
    CData/*7:0*/ __VdlyVal__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v3;
    __VdlyVal__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v3 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v3;
    __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v3 = 0;
    CData/*7:0*/ __VdlyVal__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v4;
    __VdlyVal__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v4 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v4;
    __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v4 = 0;
    CData/*7:0*/ __VdlyVal__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v5;
    __VdlyVal__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v5 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v5;
    __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v5 = 0;
    CData/*7:0*/ __VdlyVal__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v6;
    __VdlyVal__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v6 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v6;
    __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v6 = 0;
    CData/*7:0*/ __VdlyVal__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v7;
    __VdlyVal__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v7 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v7;
    __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v7 = 0;
    CData/*7:0*/ __VdlyVal__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v8;
    __VdlyVal__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v8 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v8;
    __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v8 = 0;
    CData/*7:0*/ __VdlyVal__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v10;
    __VdlyVal__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v10 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v10;
    __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v10 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v11;
    __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v11 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v12;
    __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v12 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v13;
    __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v13 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v14;
    __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v14 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v15;
    __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v15 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v16;
    __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v16 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v17;
    __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v17 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v18;
    __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v18 = 0;
    CData/*7:0*/ __VdlyVal__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v0;
    __VdlyVal__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v0 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v0;
    __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v0 = 0;
    CData/*7:0*/ __VdlyVal__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v1;
    __VdlyVal__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v1 = 0;
    CData/*2:0*/ __VdlyDim0__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v1;
    __VdlyDim0__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v1 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v1;
    __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v1 = 0;
    CData/*7:0*/ __VdlyVal__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v2;
    __VdlyVal__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v2 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v2;
    __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v2 = 0;
    CData/*7:0*/ __VdlyVal__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v3;
    __VdlyVal__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v3 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v3;
    __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v3 = 0;
    CData/*7:0*/ __VdlyVal__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v4;
    __VdlyVal__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v4 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v4;
    __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v4 = 0;
    CData/*7:0*/ __VdlyVal__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v5;
    __VdlyVal__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v5 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v5;
    __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v5 = 0;
    CData/*7:0*/ __VdlyVal__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v6;
    __VdlyVal__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v6 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v6;
    __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v6 = 0;
    CData/*7:0*/ __VdlyVal__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v7;
    __VdlyVal__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v7 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v7;
    __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v7 = 0;
    CData/*7:0*/ __VdlyVal__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v8;
    __VdlyVal__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v8 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v8;
    __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v8 = 0;
    CData/*7:0*/ __VdlyVal__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v10;
    __VdlyVal__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v10 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v10;
    __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v10 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v11;
    __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v11 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v12;
    __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v12 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v13;
    __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v13 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v14;
    __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v14 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v15;
    __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v15 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v16;
    __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v16 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v17;
    __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v17 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v18;
    __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v18 = 0;
    CData/*7:0*/ __VdlyVal__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v0;
    __VdlyVal__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v0 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v0;
    __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v0 = 0;
    CData/*7:0*/ __VdlyVal__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v1;
    __VdlyVal__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v1 = 0;
    CData/*2:0*/ __VdlyDim0__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v1;
    __VdlyDim0__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v1 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v1;
    __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v1 = 0;
    CData/*7:0*/ __VdlyVal__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v2;
    __VdlyVal__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v2 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v2;
    __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v2 = 0;
    CData/*7:0*/ __VdlyVal__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v3;
    __VdlyVal__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v3 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v3;
    __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v3 = 0;
    CData/*7:0*/ __VdlyVal__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v4;
    __VdlyVal__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v4 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v4;
    __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v4 = 0;
    CData/*7:0*/ __VdlyVal__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v5;
    __VdlyVal__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v5 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v5;
    __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v5 = 0;
    CData/*7:0*/ __VdlyVal__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v6;
    __VdlyVal__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v6 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v6;
    __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v6 = 0;
    CData/*7:0*/ __VdlyVal__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v7;
    __VdlyVal__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v7 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v7;
    __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v7 = 0;
    CData/*7:0*/ __VdlyVal__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v8;
    __VdlyVal__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v8 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v8;
    __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v8 = 0;
    CData/*7:0*/ __VdlyVal__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v10;
    __VdlyVal__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v10 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v10;
    __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v10 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v11;
    __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v11 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v12;
    __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v12 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v13;
    __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v13 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v14;
    __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v14 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v15;
    __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v15 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v16;
    __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v16 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v17;
    __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v17 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v18;
    __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v18 = 0;
    CData/*7:0*/ __VdlyVal__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v0;
    __VdlyVal__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v0 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v0;
    __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v0 = 0;
    CData/*7:0*/ __VdlyVal__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v1;
    __VdlyVal__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v1 = 0;
    CData/*2:0*/ __VdlyDim0__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v1;
    __VdlyDim0__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v1 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v1;
    __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v1 = 0;
    CData/*7:0*/ __VdlyVal__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v2;
    __VdlyVal__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v2 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v2;
    __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v2 = 0;
    CData/*7:0*/ __VdlyVal__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v3;
    __VdlyVal__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v3 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v3;
    __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v3 = 0;
    CData/*7:0*/ __VdlyVal__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v4;
    __VdlyVal__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v4 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v4;
    __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v4 = 0;
    CData/*7:0*/ __VdlyVal__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v5;
    __VdlyVal__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v5 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v5;
    __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v5 = 0;
    CData/*7:0*/ __VdlyVal__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v6;
    __VdlyVal__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v6 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v6;
    __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v6 = 0;
    CData/*7:0*/ __VdlyVal__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v7;
    __VdlyVal__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v7 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v7;
    __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v7 = 0;
    CData/*7:0*/ __VdlyVal__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v8;
    __VdlyVal__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v8 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v8;
    __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v8 = 0;
    CData/*7:0*/ __VdlyVal__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v10;
    __VdlyVal__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v10 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v10;
    __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v10 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v11;
    __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v11 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v12;
    __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v12 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v13;
    __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v13 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v14;
    __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v14 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v15;
    __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v15 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v16;
    __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v16 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v17;
    __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v17 = 0;
    CData/*0:0*/ __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v18;
    __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v18 = 0;
    // Body
    __Vdly__u_core__DOT__tick_pend = vlSelfRef.u_core__DOT__tick_pend;
    __Vdly__u_egbuf__DOT__a_v = vlSelfRef.u_egbuf__DOT__a_v;
    __VdlySet__u_core__DOT__u_rq__DOT__R__v0 = 0U;
    __VdlySet__u_core__DOT__u_rq__DOT__R__v1 = 0U;
    __VdlySet__u_core__DOT__u_rq__DOT__R__v2 = 0U;
    __Vdly__u_inbuf__DOT__a_v = vlSelfRef.u_inbuf__DOT__a_v;
    __Vdly__u_core__DOT__refr = vlSelfRef.u_core__DOT__refr;
    __Vdly__u_core__DOT__eidx = vlSelfRef.u_core__DOT__eidx;
    __Vdly__u_core__DOT__wacc = vlSelfRef.u_core__DOT__wacc;
    __Vdly__u_core__DOT__state = vlSelfRef.u_core__DOT__state;
    __VdlySet__u_core__DOT__etab__v0 = 0U;
    __VdlySet__u_core__DOT__etab__v1 = 0U;
    __Vdly__u_core__DOT__ci_ready = vlSelfRef.u_core__DOT__ci_ready;
    __Vdly__u_core__DOT__lx_valid = vlSelfRef.u_core__DOT__lx_valid;
    __Vdly__u_core__DOT__act = vlSelfRef.u_core__DOT__act;
    __Vdly__u_core__DOT__lo_valid = vlSelfRef.u_core__DOT__lo_valid;
    __VdlySet__u_df__DOT__dial__v0 = 0U;
    __VdlySet__u_df__DOT__dial__v1 = 0U;
    __Vdly__edges__BRA__1__KET____DOT__u_hebb__DOT__hl_cnt 
        = vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__hl_cnt;
    __Vdly__edges__BRA__2__KET____DOT__u_hebb__DOT__hl_cnt 
        = vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__hl_cnt;
    __Vdly__edges__BRA__3__KET____DOT__u_hebb__DOT__hl_cnt 
        = vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__hl_cnt;
    __Vdly__edges__BRA__1__KET____DOT__u_hebb__DOT__age 
        = vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__age;
    __Vdly__edges__BRA__2__KET____DOT__u_hebb__DOT__age 
        = vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__age;
    __Vdly__edges__BRA__3__KET____DOT__u_hebb__DOT__age 
        = vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__age;
    __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v0 = 0U;
    __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v1 = 0U;
    __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v2 = 0U;
    __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v3 = 0U;
    __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v4 = 0U;
    __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v5 = 0U;
    __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v6 = 0U;
    __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v7 = 0U;
    __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v8 = 0U;
    __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v10 = 0U;
    __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v11 = 0U;
    __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v12 = 0U;
    __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v13 = 0U;
    __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v14 = 0U;
    __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v15 = 0U;
    __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v16 = 0U;
    __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v17 = 0U;
    __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v18 = 0U;
    __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v0 = 0U;
    __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v1 = 0U;
    __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v2 = 0U;
    __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v3 = 0U;
    __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v4 = 0U;
    __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v5 = 0U;
    __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v6 = 0U;
    __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v7 = 0U;
    __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v8 = 0U;
    __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v10 = 0U;
    __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v11 = 0U;
    __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v12 = 0U;
    __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v13 = 0U;
    __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v14 = 0U;
    __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v15 = 0U;
    __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v16 = 0U;
    __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v17 = 0U;
    __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v18 = 0U;
    __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v0 = 0U;
    __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v1 = 0U;
    __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v2 = 0U;
    __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v3 = 0U;
    __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v4 = 0U;
    __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v5 = 0U;
    __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v6 = 0U;
    __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v7 = 0U;
    __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v8 = 0U;
    __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v10 = 0U;
    __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v11 = 0U;
    __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v12 = 0U;
    __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v13 = 0U;
    __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v14 = 0U;
    __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v15 = 0U;
    __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v16 = 0U;
    __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v17 = 0U;
    __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v18 = 0U;
    __Vdly__edges__BRA__1__KET____DOT__u_hebb__DOT__wh 
        = vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__wh;
    __Vdly__edges__BRA__2__KET____DOT__u_hebb__DOT__wh 
        = vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__wh;
    __Vdly__edges__BRA__3__KET____DOT__u_hebb__DOT__wh 
        = vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__wh;
    __Vdly__edges__BRA__0__KET____DOT__u_hebb__DOT__hl_cnt 
        = vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__hl_cnt;
    __Vdly__edges__BRA__0__KET____DOT__u_hebb__DOT__age 
        = vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__age;
    __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v0 = 0U;
    __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v1 = 0U;
    __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v2 = 0U;
    __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v3 = 0U;
    __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v4 = 0U;
    __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v5 = 0U;
    __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v6 = 0U;
    __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v7 = 0U;
    __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v8 = 0U;
    __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v10 = 0U;
    __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v11 = 0U;
    __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v12 = 0U;
    __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v13 = 0U;
    __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v14 = 0U;
    __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v15 = 0U;
    __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v16 = 0U;
    __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v17 = 0U;
    __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v18 = 0U;
    __Vdly__edges__BRA__0__KET____DOT__u_hebb__DOT__wh 
        = vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__wh;
    if ((1U & (~ (IData)(vlSelfRef.rst_n)))) {
        vlSelfRef.u_core__DOT__i = 1U;
        vlSelfRef.u_core__DOT__i = 2U;
        vlSelfRef.u_core__DOT__i = 3U;
        vlSelfRef.u_core__DOT__i = 4U;
        vlSelfRef.u_core__DOT__u_rq__DOT__j = 1U;
        vlSelfRef.u_core__DOT__u_rq__DOT__j = 2U;
        vlSelfRef.u_core__DOT__u_rq__DOT__j = 3U;
        vlSelfRef.u_core__DOT__u_rq__DOT__j = 4U;
    }
    if (vlSelfRef.rst_n) {
        if (vlSelfRef.s_tick) {
            __Vdly__u_core__DOT__tick_pend = 1U;
        } else if (((2U == (IData)(vlSelfRef.u_core__DOT__state)) 
                    & (IData)(vlSelfRef.u_core__DOT__tick_pend))) {
            __Vdly__u_core__DOT__tick_pend = 0U;
        }
        if (vlSelfRef.d_rqen) {
            if (vlSelfRef.u_core__DOT__rq_train) {
                __VdlyVal__u_core__DOT__u_rq__DOT__R__v0 
                    = vlSelfRef.u_core__DOT__u_rq__DOT__rdepn;
                __VdlyDim0__u_core__DOT__u_rq__DOT__R__v0 
                    = vlSelfRef.u_core__DOT__u_rq__DOT__esel;
                __VdlySet__u_core__DOT__u_rq__DOT__R__v0 = 1U;
            } else if (vlSelfRef.u_core__DOT__rq_tick) {
                __VdlyVal__u_core__DOT__u_rq__DOT__R__v1 
                    = vlSelfRef.u_core__DOT__u_rq__DOT__rleakn;
                __VdlyDim0__u_core__DOT__u_rq__DOT__R__v1 
                    = vlSelfRef.u_core__DOT__u_rq__DOT__esel;
                __VdlySet__u_core__DOT__u_rq__DOT__R__v1 = 1U;
            }
        }
        if (vlSelfRef.u_egbuf__DOT__pop) {
            __Vdly__u_egbuf__DOT__a_v = vlSelfRef.u_egbuf__DOT__b_v;
            vlSelfRef.u_egbuf__DOT__a_q[0U] = vlSelfRef.u_egbuf__DOT__b_q[0U];
            vlSelfRef.u_egbuf__DOT__a_q[1U] = vlSelfRef.u_egbuf__DOT__b_q[1U];
            vlSelfRef.u_egbuf__DOT__a_q[2U] = vlSelfRef.u_egbuf__DOT__b_q[2U];
            vlSelfRef.u_egbuf__DOT__b_v = 0U;
        }
        if (vlSelfRef.u_egbuf__DOT__push) {
            if (((IData)(vlSelfRef.u_egbuf__DOT__a_v) 
                 & (~ (IData)(vlSelfRef.u_egbuf__DOT__pop)))) {
                vlSelfRef.u_egbuf__DOT__b_q[0U] = vlSelfRef.u_egbuf__DOT__s_bus[0U];
                vlSelfRef.u_egbuf__DOT__b_q[1U] = vlSelfRef.u_egbuf__DOT__s_bus[1U];
                vlSelfRef.u_egbuf__DOT__b_q[2U] = vlSelfRef.u_egbuf__DOT__s_bus[2U];
                vlSelfRef.u_egbuf__DOT__b_v = 1U;
            } else {
                vlSelfRef.u_egbuf__DOT__a_q[0U] = vlSelfRef.u_egbuf__DOT__s_bus[0U];
                vlSelfRef.u_egbuf__DOT__a_q[1U] = vlSelfRef.u_egbuf__DOT__s_bus[1U];
                vlSelfRef.u_egbuf__DOT__a_q[2U] = vlSelfRef.u_egbuf__DOT__s_bus[2U];
                __Vdly__u_egbuf__DOT__a_v = 1U;
            }
        }
        if (vlSelfRef.u_inbuf__DOT__pop) {
            __Vdly__u_inbuf__DOT__a_v = vlSelfRef.u_inbuf__DOT__b_v;
            vlSelfRef.u_inbuf__DOT__a_q[0U] = vlSelfRef.u_inbuf__DOT__b_q[0U];
            vlSelfRef.u_inbuf__DOT__a_q[1U] = vlSelfRef.u_inbuf__DOT__b_q[1U];
            vlSelfRef.u_inbuf__DOT__a_q[2U] = vlSelfRef.u_inbuf__DOT__b_q[2U];
            vlSelfRef.u_inbuf__DOT__b_v = 0U;
        }
        if (vlSelfRef.u_inbuf__DOT__push) {
            if (((IData)(vlSelfRef.u_inbuf__DOT__a_v) 
                 & (~ (IData)(vlSelfRef.u_inbuf__DOT__pop)))) {
                vlSelfRef.u_inbuf__DOT__b_q[0U] = vlSelfRef.u_inbuf__DOT__s_bus[0U];
                vlSelfRef.u_inbuf__DOT__b_q[1U] = vlSelfRef.u_inbuf__DOT__s_bus[1U];
                vlSelfRef.u_inbuf__DOT__b_q[2U] = vlSelfRef.u_inbuf__DOT__s_bus[2U];
                vlSelfRef.u_inbuf__DOT__b_v = 1U;
            } else {
                vlSelfRef.u_inbuf__DOT__a_q[0U] = vlSelfRef.u_inbuf__DOT__s_bus[0U];
                vlSelfRef.u_inbuf__DOT__a_q[1U] = vlSelfRef.u_inbuf__DOT__s_bus[1U];
                vlSelfRef.u_inbuf__DOT__a_q[2U] = vlSelfRef.u_inbuf__DOT__s_bus[2U];
                __Vdly__u_inbuf__DOT__a_v = 1U;
            }
        }
        if (vlSelfRef.u_core__DOT__eg_fire) {
            vlSelfRef.u_core__DOT__u_eg__DOT__f = 0xffffU;
        } else if (vlSelfRef.u_core__DOT__eg_tick) {
            vlSelfRef.u_core__DOT__u_eg__DOT__f = ((IData)(vlSelfRef.u_core__DOT__u_eg__DOT__fsnap)
                                                    ? 0U
                                                    : (IData)(vlSelfRef.u_core__DOT__u_eg__DOT__fleak));
        }
        vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__o_done = 0U;
        if (vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__rstate) {
            if ((8U == (IData)(vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__ridx))) {
                vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__o_w 
                    = vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__wout;
                vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__o_done = 1U;
                vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__rstate = 0U;
            } else {
                vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__acc 
                    = (0x1ffffU & (vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__acc 
                                   + vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__addw));
                vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__ridx 
                    = (0x1fU & ((IData)(1U) + (IData)(vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__ridx)));
            }
        } else if ((2U & (IData)(vlSelfRef.u_core__DOT__hb_sel))) {
            if ((4U & (IData)(vlSelfRef.hb_cmd))) {
                if ((1U & (~ ((IData)(vlSelfRef.hb_cmd) 
                              >> 1U)))) {
                    if ((1U & (IData)(vlSelfRef.hb_cmd))) {
                        if (vlSelfRef.d_mode) {
                            if ((0xffffU == (IData)(vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__wh))) {
                                vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__o_ovf = 1U;
                            } else {
                                __Vdly__edges__BRA__1__KET____DOT__u_hebb__DOT__wh 
                                    = (0xffffU & ((IData)(1U) 
                                                  + (IData)(vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__wh)));
                            }
                        } else if ((8U <= (IData)(vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__gcl))) {
                            if ((0xffU == vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__c
                                 [7U])) {
                                vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__o_ovf = 1U;
                            } else {
                                __VdlyVal__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v0 
                                    = (0xffU & ((IData)(1U) 
                                                + vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__c
                                                [7U]));
                                __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v0 = 1U;
                            }
                        } else if ((0xffU == vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__c
                                    [(7U & (IData)(vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__gcl))])) {
                            vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__o_ovf = 1U;
                        } else {
                            __VdlyVal__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v1 
                                = (0xffU & ((IData)(1U) 
                                            + vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__c
                                            [(7U & (IData)(vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__gcl))]));
                            __VdlyDim0__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v1 
                                = (7U & (IData)(vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__gcl));
                            __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v1 = 1U;
                        }
                        vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__o_done = 1U;
                    } else {
                        vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__base 
                            = vlSelfRef.hb_base;
                        vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__o_done = 1U;
                    }
                }
            } else if ((2U & (IData)(vlSelfRef.hb_cmd))) {
                if ((1U & (IData)(vlSelfRef.hb_cmd))) {
                    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__ridx = 0U;
                    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__acc = 0U;
                    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__rstate = 1U;
                } else {
                    if (vlSelfRef.d_mode) {
                        if (vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__decn) {
                            __Vdly__edges__BRA__1__KET____DOT__u_hebb__DOT__wh 
                                = (0xffffU & ((IData)(vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__wh) 
                                              - (IData)(1U)));
                            __Vdly__edges__BRA__1__KET____DOT__u_hebb__DOT__age = 0U;
                        } else {
                            __Vdly__edges__BRA__1__KET____DOT__u_hebb__DOT__age 
                                = (0xffffffU & ((IData)(1U) 
                                                + vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__age));
                        }
                    } else if (vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__hlend) {
                        vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__j = 6U;
                        __VdlyVal__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v2 
                            = vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__c
                            [6U];
                        __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v2 = 1U;
                        vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__j = 5U;
                        __Vdly__edges__BRA__1__KET____DOT__u_hebb__DOT__hl_cnt = 0U;
                        __VdlyVal__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v3 
                            = vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__c
                            [5U];
                        __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v3 = 1U;
                        vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__j = 4U;
                        __VdlyVal__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v4 
                            = vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__c
                            [4U];
                        __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v4 = 1U;
                        vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__j = 3U;
                        __VdlyVal__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v5 
                            = vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__c
                            [3U];
                        __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v5 = 1U;
                        vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__j = 2U;
                        __VdlyVal__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v6 
                            = vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__c
                            [2U];
                        __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v6 = 1U;
                        vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__j = 1U;
                        __VdlyVal__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v7 
                            = vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__c
                            [1U];
                        __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v7 = 1U;
                        vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__j = 0U;
                        __VdlyVal__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v8 
                            = vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__c
                            [0U];
                        __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v8 = 1U;
                    } else {
                        __Vdly__edges__BRA__1__KET____DOT__u_hebb__DOT__hl_cnt 
                            = (0xffffU & ((IData)(1U) 
                                          + (IData)(vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__hl_cnt)));
                    }
                    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__o_done = 1U;
                }
            } else if ((1U & (IData)(vlSelfRef.hb_cmd))) {
                if (vlSelfRef.d_mode) {
                    if ((0xffffU == (IData)(vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__wh))) {
                        vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__o_ovf = 1U;
                    } else {
                        __Vdly__edges__BRA__1__KET____DOT__u_hebb__DOT__wh 
                            = (0xffffU & ((IData)(1U) 
                                          + (IData)(vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__wh)));
                    }
                } else if ((0xffU == vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__c
                            [0U])) {
                    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__o_ovf = 1U;
                } else {
                    __VdlyVal__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v10 
                        = (0xffU & ((IData)(1U) + vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__c
                                    [0U]));
                    __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v10 = 1U;
                }
                vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__o_done = 1U;
            }
        }
        vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__o_done = 0U;
        if (vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__rstate) {
            if ((8U == (IData)(vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__ridx))) {
                vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__o_w 
                    = vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__wout;
                vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__o_done = 1U;
                vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__rstate = 0U;
            } else {
                vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__acc 
                    = (0x1ffffU & (vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__acc 
                                   + vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__addw));
                vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__ridx 
                    = (0x1fU & ((IData)(1U) + (IData)(vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__ridx)));
            }
        } else if ((4U & (IData)(vlSelfRef.u_core__DOT__hb_sel))) {
            if ((4U & (IData)(vlSelfRef.hb_cmd))) {
                if ((1U & (~ ((IData)(vlSelfRef.hb_cmd) 
                              >> 1U)))) {
                    if ((1U & (IData)(vlSelfRef.hb_cmd))) {
                        if (vlSelfRef.d_mode) {
                            if ((0xffffU == (IData)(vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__wh))) {
                                vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__o_ovf = 1U;
                            } else {
                                __Vdly__edges__BRA__2__KET____DOT__u_hebb__DOT__wh 
                                    = (0xffffU & ((IData)(1U) 
                                                  + (IData)(vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__wh)));
                            }
                        } else if ((8U <= (IData)(vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__gcl))) {
                            if ((0xffU == vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__c
                                 [7U])) {
                                vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__o_ovf = 1U;
                            } else {
                                __VdlyVal__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v0 
                                    = (0xffU & ((IData)(1U) 
                                                + vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__c
                                                [7U]));
                                __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v0 = 1U;
                            }
                        } else if ((0xffU == vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__c
                                    [(7U & (IData)(vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__gcl))])) {
                            vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__o_ovf = 1U;
                        } else {
                            __VdlyVal__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v1 
                                = (0xffU & ((IData)(1U) 
                                            + vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__c
                                            [(7U & (IData)(vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__gcl))]));
                            __VdlyDim0__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v1 
                                = (7U & (IData)(vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__gcl));
                            __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v1 = 1U;
                        }
                        vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__o_done = 1U;
                    } else {
                        vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__base 
                            = vlSelfRef.hb_base;
                        vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__o_done = 1U;
                    }
                }
            } else if ((2U & (IData)(vlSelfRef.hb_cmd))) {
                if ((1U & (IData)(vlSelfRef.hb_cmd))) {
                    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__ridx = 0U;
                    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__acc = 0U;
                    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__rstate = 1U;
                } else {
                    if (vlSelfRef.d_mode) {
                        if (vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__decn) {
                            __Vdly__edges__BRA__2__KET____DOT__u_hebb__DOT__wh 
                                = (0xffffU & ((IData)(vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__wh) 
                                              - (IData)(1U)));
                            __Vdly__edges__BRA__2__KET____DOT__u_hebb__DOT__age = 0U;
                        } else {
                            __Vdly__edges__BRA__2__KET____DOT__u_hebb__DOT__age 
                                = (0xffffffU & ((IData)(1U) 
                                                + vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__age));
                        }
                    } else if (vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__hlend) {
                        vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__j = 6U;
                        __VdlyVal__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v2 
                            = vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__c
                            [6U];
                        __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v2 = 1U;
                        vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__j = 5U;
                        __Vdly__edges__BRA__2__KET____DOT__u_hebb__DOT__hl_cnt = 0U;
                        __VdlyVal__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v3 
                            = vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__c
                            [5U];
                        __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v3 = 1U;
                        vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__j = 4U;
                        __VdlyVal__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v4 
                            = vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__c
                            [4U];
                        __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v4 = 1U;
                        vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__j = 3U;
                        __VdlyVal__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v5 
                            = vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__c
                            [3U];
                        __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v5 = 1U;
                        vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__j = 2U;
                        __VdlyVal__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v6 
                            = vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__c
                            [2U];
                        __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v6 = 1U;
                        vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__j = 1U;
                        __VdlyVal__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v7 
                            = vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__c
                            [1U];
                        __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v7 = 1U;
                        vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__j = 0U;
                        __VdlyVal__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v8 
                            = vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__c
                            [0U];
                        __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v8 = 1U;
                    } else {
                        __Vdly__edges__BRA__2__KET____DOT__u_hebb__DOT__hl_cnt 
                            = (0xffffU & ((IData)(1U) 
                                          + (IData)(vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__hl_cnt)));
                    }
                    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__o_done = 1U;
                }
            } else if ((1U & (IData)(vlSelfRef.hb_cmd))) {
                if (vlSelfRef.d_mode) {
                    if ((0xffffU == (IData)(vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__wh))) {
                        vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__o_ovf = 1U;
                    } else {
                        __Vdly__edges__BRA__2__KET____DOT__u_hebb__DOT__wh 
                            = (0xffffU & ((IData)(1U) 
                                          + (IData)(vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__wh)));
                    }
                } else if ((0xffU == vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__c
                            [0U])) {
                    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__o_ovf = 1U;
                } else {
                    __VdlyVal__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v10 
                        = (0xffU & ((IData)(1U) + vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__c
                                    [0U]));
                    __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v10 = 1U;
                }
                vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__o_done = 1U;
            }
        }
        vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__o_done = 0U;
        if (vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__rstate) {
            if ((8U == (IData)(vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__ridx))) {
                vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__o_w 
                    = vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__wout;
                vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__o_done = 1U;
                vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__rstate = 0U;
            } else {
                vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__acc 
                    = (0x1ffffU & (vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__acc 
                                   + vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__addw));
                vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__ridx 
                    = (0x1fU & ((IData)(1U) + (IData)(vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__ridx)));
            }
        } else if ((8U & (IData)(vlSelfRef.u_core__DOT__hb_sel))) {
            if ((4U & (IData)(vlSelfRef.hb_cmd))) {
                if ((1U & (~ ((IData)(vlSelfRef.hb_cmd) 
                              >> 1U)))) {
                    if ((1U & (IData)(vlSelfRef.hb_cmd))) {
                        if (vlSelfRef.d_mode) {
                            if ((0xffffU == (IData)(vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__wh))) {
                                vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__o_ovf = 1U;
                            } else {
                                __Vdly__edges__BRA__3__KET____DOT__u_hebb__DOT__wh 
                                    = (0xffffU & ((IData)(1U) 
                                                  + (IData)(vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__wh)));
                            }
                        } else if ((8U <= (IData)(vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__gcl))) {
                            if ((0xffU == vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__c
                                 [7U])) {
                                vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__o_ovf = 1U;
                            } else {
                                __VdlyVal__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v0 
                                    = (0xffU & ((IData)(1U) 
                                                + vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__c
                                                [7U]));
                                __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v0 = 1U;
                            }
                        } else if ((0xffU == vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__c
                                    [(7U & (IData)(vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__gcl))])) {
                            vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__o_ovf = 1U;
                        } else {
                            __VdlyVal__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v1 
                                = (0xffU & ((IData)(1U) 
                                            + vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__c
                                            [(7U & (IData)(vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__gcl))]));
                            __VdlyDim0__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v1 
                                = (7U & (IData)(vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__gcl));
                            __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v1 = 1U;
                        }
                        vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__o_done = 1U;
                    } else {
                        vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__base 
                            = vlSelfRef.hb_base;
                        vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__o_done = 1U;
                    }
                }
            } else if ((2U & (IData)(vlSelfRef.hb_cmd))) {
                if ((1U & (IData)(vlSelfRef.hb_cmd))) {
                    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__ridx = 0U;
                    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__acc = 0U;
                    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__rstate = 1U;
                } else {
                    if (vlSelfRef.d_mode) {
                        if (vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__decn) {
                            __Vdly__edges__BRA__3__KET____DOT__u_hebb__DOT__wh 
                                = (0xffffU & ((IData)(vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__wh) 
                                              - (IData)(1U)));
                            __Vdly__edges__BRA__3__KET____DOT__u_hebb__DOT__age = 0U;
                        } else {
                            __Vdly__edges__BRA__3__KET____DOT__u_hebb__DOT__age 
                                = (0xffffffU & ((IData)(1U) 
                                                + vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__age));
                        }
                    } else if (vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__hlend) {
                        vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__j = 6U;
                        __VdlyVal__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v2 
                            = vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__c
                            [6U];
                        __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v2 = 1U;
                        vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__j = 5U;
                        __Vdly__edges__BRA__3__KET____DOT__u_hebb__DOT__hl_cnt = 0U;
                        __VdlyVal__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v3 
                            = vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__c
                            [5U];
                        __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v3 = 1U;
                        vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__j = 4U;
                        __VdlyVal__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v4 
                            = vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__c
                            [4U];
                        __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v4 = 1U;
                        vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__j = 3U;
                        __VdlyVal__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v5 
                            = vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__c
                            [3U];
                        __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v5 = 1U;
                        vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__j = 2U;
                        __VdlyVal__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v6 
                            = vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__c
                            [2U];
                        __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v6 = 1U;
                        vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__j = 1U;
                        __VdlyVal__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v7 
                            = vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__c
                            [1U];
                        __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v7 = 1U;
                        vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__j = 0U;
                        __VdlyVal__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v8 
                            = vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__c
                            [0U];
                        __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v8 = 1U;
                    } else {
                        __Vdly__edges__BRA__3__KET____DOT__u_hebb__DOT__hl_cnt 
                            = (0xffffU & ((IData)(1U) 
                                          + (IData)(vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__hl_cnt)));
                    }
                    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__o_done = 1U;
                }
            } else if ((1U & (IData)(vlSelfRef.hb_cmd))) {
                if (vlSelfRef.d_mode) {
                    if ((0xffffU == (IData)(vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__wh))) {
                        vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__o_ovf = 1U;
                    } else {
                        __Vdly__edges__BRA__3__KET____DOT__u_hebb__DOT__wh 
                            = (0xffffU & ((IData)(1U) 
                                          + (IData)(vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__wh)));
                    }
                } else if ((0xffU == vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__c
                            [0U])) {
                    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__o_ovf = 1U;
                } else {
                    __VdlyVal__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v10 
                        = (0xffU & ((IData)(1U) + vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__c
                                    [0U]));
                    __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v10 = 1U;
                }
                vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__o_done = 1U;
            }
        }
        vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__o_done = 0U;
        if (vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__rstate) {
            if ((8U == (IData)(vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__ridx))) {
                vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__o_w 
                    = vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__wout;
                vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__o_done = 1U;
                vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__rstate = 0U;
            } else {
                vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__acc 
                    = (0x1ffffU & (vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__acc 
                                   + vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__addw));
                vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__ridx 
                    = (0x1fU & ((IData)(1U) + (IData)(vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__ridx)));
            }
        } else if ((1U & (IData)(vlSelfRef.u_core__DOT__hb_sel))) {
            if ((4U & (IData)(vlSelfRef.hb_cmd))) {
                if ((1U & (~ ((IData)(vlSelfRef.hb_cmd) 
                              >> 1U)))) {
                    if ((1U & (IData)(vlSelfRef.hb_cmd))) {
                        if (vlSelfRef.d_mode) {
                            if ((0xffffU == (IData)(vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__wh))) {
                                vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__o_ovf = 1U;
                            } else {
                                __Vdly__edges__BRA__0__KET____DOT__u_hebb__DOT__wh 
                                    = (0xffffU & ((IData)(1U) 
                                                  + (IData)(vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__wh)));
                            }
                        } else if ((8U <= (IData)(vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__gcl))) {
                            if ((0xffU == vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__c
                                 [7U])) {
                                vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__o_ovf = 1U;
                            } else {
                                __VdlyVal__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v0 
                                    = (0xffU & ((IData)(1U) 
                                                + vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__c
                                                [7U]));
                                __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v0 = 1U;
                            }
                        } else if ((0xffU == vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__c
                                    [(7U & (IData)(vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__gcl))])) {
                            vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__o_ovf = 1U;
                        } else {
                            __VdlyVal__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v1 
                                = (0xffU & ((IData)(1U) 
                                            + vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__c
                                            [(7U & (IData)(vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__gcl))]));
                            __VdlyDim0__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v1 
                                = (7U & (IData)(vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__gcl));
                            __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v1 = 1U;
                        }
                        vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__o_done = 1U;
                    } else {
                        vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__base 
                            = vlSelfRef.hb_base;
                        vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__o_done = 1U;
                    }
                }
            } else if ((2U & (IData)(vlSelfRef.hb_cmd))) {
                if ((1U & (IData)(vlSelfRef.hb_cmd))) {
                    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__ridx = 0U;
                    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__acc = 0U;
                    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__rstate = 1U;
                } else {
                    if (vlSelfRef.d_mode) {
                        if (vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__decn) {
                            __Vdly__edges__BRA__0__KET____DOT__u_hebb__DOT__wh 
                                = (0xffffU & ((IData)(vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__wh) 
                                              - (IData)(1U)));
                            __Vdly__edges__BRA__0__KET____DOT__u_hebb__DOT__age = 0U;
                        } else {
                            __Vdly__edges__BRA__0__KET____DOT__u_hebb__DOT__age 
                                = (0xffffffU & ((IData)(1U) 
                                                + vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__age));
                        }
                    } else if (vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__hlend) {
                        vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__j = 6U;
                        __VdlyVal__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v2 
                            = vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__c
                            [6U];
                        __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v2 = 1U;
                        vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__j = 5U;
                        __Vdly__edges__BRA__0__KET____DOT__u_hebb__DOT__hl_cnt = 0U;
                        __VdlyVal__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v3 
                            = vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__c
                            [5U];
                        __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v3 = 1U;
                        vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__j = 4U;
                        __VdlyVal__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v4 
                            = vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__c
                            [4U];
                        __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v4 = 1U;
                        vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__j = 3U;
                        __VdlyVal__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v5 
                            = vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__c
                            [3U];
                        __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v5 = 1U;
                        vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__j = 2U;
                        __VdlyVal__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v6 
                            = vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__c
                            [2U];
                        __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v6 = 1U;
                        vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__j = 1U;
                        __VdlyVal__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v7 
                            = vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__c
                            [1U];
                        __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v7 = 1U;
                        vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__j = 0U;
                        __VdlyVal__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v8 
                            = vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__c
                            [0U];
                        __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v8 = 1U;
                    } else {
                        __Vdly__edges__BRA__0__KET____DOT__u_hebb__DOT__hl_cnt 
                            = (0xffffU & ((IData)(1U) 
                                          + (IData)(vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__hl_cnt)));
                    }
                    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__o_done = 1U;
                }
            } else if ((1U & (IData)(vlSelfRef.hb_cmd))) {
                if (vlSelfRef.d_mode) {
                    if ((0xffffU == (IData)(vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__wh))) {
                        vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__o_ovf = 1U;
                    } else {
                        __Vdly__edges__BRA__0__KET____DOT__u_hebb__DOT__wh 
                            = (0xffffU & ((IData)(1U) 
                                          + (IData)(vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__wh)));
                    }
                } else if ((0xffU == vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__c
                            [0U])) {
                    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__o_ovf = 1U;
                } else {
                    __VdlyVal__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v10 
                        = (0xffU & ((IData)(1U) + vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__c
                                    [0U]));
                    __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v10 = 1U;
                }
                vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__o_done = 1U;
            }
        }
        vlSelfRef.u_core__DOT__df_wr = 0U;
        vlSelfRef.u_core__DOT__df_rd = 0U;
        vlSelfRef.u_core__DOT__hb_cmd = 0U;
        vlSelfRef.u_core__DOT__eg_fire = 0U;
        __Vdly__u_core__DOT__lo_valid = 0U;
        __Vdly__u_core__DOT__lx_valid = 0U;
        if ((0x10U & (IData)(vlSelfRef.u_core__DOT__state))) {
            if ((8U & (IData)(vlSelfRef.u_core__DOT__state))) {
                __Vdly__u_core__DOT__state = 2U;
            } else if ((4U & (IData)(vlSelfRef.u_core__DOT__state))) {
                if ((2U & (IData)(vlSelfRef.u_core__DOT__state))) {
                    __Vdly__u_core__DOT__state = 2U;
                } else if ((1U & (IData)(vlSelfRef.u_core__DOT__state))) {
                    vlSelfRef.u_core__DOT__eff_p = vlSelfRef.u_core__DOT__prod_p;
                    __Vdly__u_core__DOT__state = 0x13U;
                } else if (vlSelfRef.hb_done) {
                    vlSelfRef.u_core__DOT__eff_w = vlSelfRef.u_core__DOT__hb_wq;
                    __Vdly__u_core__DOT__state = 0x15U;
                }
            } else if ((2U & (IData)(vlSelfRef.u_core__DOT__state))) {
                if ((1U & (IData)(vlSelfRef.u_core__DOT__state))) {
                    __Vfunc_u_core__DOT__sclip16__35__v 
                        = (0xfffffffffULL & (vlSelfRef.u_core__DOT__act_e 
                                             + VL_SHIFTRS_QQI(36,36,32, vlSelfRef.u_core__DOT__eff_pe, 0xfU)));
                    __Vfunc_u_core__DOT__sclip16__35__Vfuncout 
                        = (VL_LTS_IQQ(36, 0x7fffULL, __Vfunc_u_core__DOT__sclip16__35__v)
                            ? 0x7fffU : (VL_GTS_IQQ(36, 0xfffff8000ULL, __Vfunc_u_core__DOT__sclip16__35__v)
                                          ? 0x8000U
                                          : (0xffffU 
                                             & (IData)(__Vfunc_u_core__DOT__sclip16__35__v))));
                    __Vdly__u_core__DOT__act = __Vfunc_u_core__DOT__sclip16__35__Vfuncout;
                    __Vdly__u_core__DOT__ci_ready = 
                        (1U & (~ ((IData)(vlSelfRef.s_tick) 
                                  | (IData)(vlSelfRef.u_core__DOT__tick_pend))));
                    __Vdly__u_core__DOT__state = 2U;
                } else if ((4U == (IData)(vlSelfRef.u_core__DOT__eidx))) {
                    __Vdly__u_core__DOT__act = 0U;
                    __Vdly__u_core__DOT__refr = vlSelfRef.d_refr;
                    __Vdly__u_core__DOT__ci_ready = 
                        (1U & (~ ((IData)(vlSelfRef.s_tick) 
                                  | (IData)(vlSelfRef.u_core__DOT__tick_pend))));
                    __Vdly__u_core__DOT__state = 2U;
                } else if (vlSelfRef.u_core__DOT__ev
                           [(3U & (IData)(vlSelfRef.u_core__DOT__eidx))]) {
                    __Vdly__u_core__DOT__lx_valid = 1U;
                    vlSelfRef.u_core__DOT__lx_op = 2U;
                    vlSelfRef.u_core__DOT__lx_dst = 
                        vlSelfRef.u_core__DOT__etab
                        [(3U & (IData)(vlSelfRef.u_core__DOT__eidx))];
                    vlSelfRef.u_core__DOT__lx_src = vlSelfRef.u_core__DOT__cell_id;
                    vlSelfRef.u_core__DOT__lx_dat = vlSelfRef.u_core__DOT__afire;
                    vlSelfRef.u_core__DOT__lx_a0 = 0U;
                    vlSelfRef.u_core__DOT__lx_a1 = 0U;
                    vlSelfRef.u_core__DOT__lx_a2 = 0U;
                    if (((IData)(vlSelfRef.u_core__DOT__lx_valid) 
                         & (IData)(vlSelfRef.lx_grant))) {
                        __Vdly__u_core__DOT__eidx = 
                            (7U & ((IData)(1U) + (IData)(vlSelfRef.u_core__DOT__eidx)));
                        __Vdly__u_core__DOT__lx_valid = 0U;
                    }
                } else {
                    __Vdly__u_core__DOT__eidx = (7U 
                                                 & ((IData)(1U) 
                                                    + (IData)(vlSelfRef.u_core__DOT__eidx)));
                }
            } else if ((1U & (IData)(vlSelfRef.u_core__DOT__state))) {
                __Vfunc_u_core__DOT__sclip16__36__v 
                    = vlSelfRef.u_core__DOT__leak_sum;
                __Vfunc_u_core__DOT__sclip16__36__Vfuncout 
                    = (VL_LTS_IQQ(36, 0x7fffULL, __Vfunc_u_core__DOT__sclip16__36__v)
                        ? 0x7fffU : (VL_GTS_IQQ(36, 0xfffff8000ULL, __Vfunc_u_core__DOT__sclip16__36__v)
                                      ? 0x8000U : (0xffffU 
                                                   & (IData)(__Vfunc_u_core__DOT__sclip16__36__v))));
                if ((VL_GTES_III(16, (IData)(vlSelfRef.u_core__DOT__act), (IData)(vlSelfRef.d_thresh)) 
                     & (0U == (IData)(vlSelfRef.u_core__DOT__refr)))) {
                    __Vdly__u_core__DOT__eidx = 0U;
                    vlSelfRef.u_core__DOT__afire = vlSelfRef.u_core__DOT__act;
                    vlSelfRef.u_core__DOT__eg_fire = 1U;
                    __Vdly__u_core__DOT__state = 0x12U;
                } else {
                    if ((0U != (IData)(vlSelfRef.u_core__DOT__refr))) {
                        __Vdly__u_core__DOT__refr = 
                            (0xffffU & ((IData)(vlSelfRef.u_core__DOT__refr) 
                                        - (IData)(1U)));
                    }
                    __Vdly__u_core__DOT__ci_ready = 
                        (1U & (~ ((IData)(vlSelfRef.s_tick) 
                                  | (IData)(vlSelfRef.u_core__DOT__tick_pend))));
                    __Vdly__u_core__DOT__state = 2U;
                }
                __Vdly__u_core__DOT__act = __Vfunc_u_core__DOT__sclip16__36__Vfuncout;
            } else if (vlSelfRef.hb_done) {
                __Vdly__u_core__DOT__eidx = (7U & ((IData)(1U) 
                                                   + (IData)(vlSelfRef.u_core__DOT__eidx)));
                __Vdly__u_core__DOT__state = 0xfU;
            }
        } else if ((8U & (IData)(vlSelfRef.u_core__DOT__state))) {
            if ((4U & (IData)(vlSelfRef.u_core__DOT__state))) {
                if ((2U & (IData)(vlSelfRef.u_core__DOT__state))) {
                    if ((1U & (IData)(vlSelfRef.u_core__DOT__state))) {
                        if ((4U == (IData)(vlSelfRef.u_core__DOT__eidx))) {
                            __Vdly__u_core__DOT__state = 0x11U;
                        } else if (vlSelfRef.u_core__DOT__ev
                                   [(3U & (IData)(vlSelfRef.u_core__DOT__eidx))]) {
                            vlSelfRef.u_core__DOT__hb_sel 
                                = (0xfU & ((IData)(1U) 
                                           << (3U & (IData)(vlSelfRef.u_core__DOT__eidx))));
                            vlSelfRef.u_core__DOT__hb_cmd = 2U;
                            __Vdly__u_core__DOT__state = 0x10U;
                        } else {
                            __Vdly__u_core__DOT__eidx 
                                = (7U & ((IData)(1U) 
                                         + (IData)(vlSelfRef.u_core__DOT__eidx)));
                        }
                    } else {
                        __Vdly__u_core__DOT__eidx = 0U;
                        __Vdly__u_core__DOT__state = 0xfU;
                    }
                } else if ((1U & (IData)(vlSelfRef.u_core__DOT__state))) {
                    __Vdly__u_core__DOT__lo_valid = 1U;
                    vlSelfRef.u_core__DOT__lo_op = 
                        ((IData)(vlSelfRef.u_core__DOT__resp_nak)
                          ? 6U : 5U);
                    vlSelfRef.u_core__DOT__lo_dst = vlSelfRef.u_core__DOT__lr_src;
                    vlSelfRef.u_core__DOT__lo_src = vlSelfRef.u_core__DOT__cell_id;
                    vlSelfRef.u_core__DOT__lo_a0 = 0U;
                    vlSelfRef.u_core__DOT__lo_a1 = 0U;
                    vlSelfRef.u_core__DOT__lo_a2 = vlSelfRef.u_core__DOT__lr_a2;
                    vlSelfRef.u_core__DOT__lo_dat = vlSelfRef.u_core__DOT__viewdat;
                    if (((IData)(vlSelfRef.u_core__DOT__lo_valid) 
                         & (IData)(vlSelfRef.lo_grant))) {
                        __Vdly__u_core__DOT__lo_valid = 0U;
                        __Vdly__u_core__DOT__ci_ready 
                            = (1U & (~ ((IData)(vlSelfRef.s_tick) 
                                        | (IData)(vlSelfRef.u_core__DOT__tick_pend))));
                        __Vdly__u_core__DOT__state = 2U;
                    }
                } else if (vlSelfRef.df_rstb) {
                    vlSelfRef.u_core__DOT__viewdat 
                        = vlSelfRef.df_rdata;
                    vlSelfRef.u_core__DOT__resp_nak = 0U;
                    __Vdly__u_core__DOT__state = 0xdU;
                }
            } else if ((2U & (IData)(vlSelfRef.u_core__DOT__state))) {
                if ((1U & (IData)(vlSelfRef.u_core__DOT__state))) {
                    if (vlSelfRef.hb_done) {
                        __Vdly__u_core__DOT__wacc = 
                            (0x7ffffU & ((vlSelfRef.u_core__DOT__wacc 
                                          + (IData)(vlSelfRef.hb_w)) 
                                         + (IData)(vlSelfRef.u_core__DOT__rq_credit)));
                        __Vdly__u_core__DOT__eidx = 
                            (7U & ((IData)(1U) + (IData)(vlSelfRef.u_core__DOT__eidx)));
                        __Vdly__u_core__DOT__state = 0xaU;
                    }
                } else if ((4U == (IData)(vlSelfRef.u_core__DOT__eidx))) {
                    vlSelfRef.u_core__DOT__viewdat 
                        = ((0U != (7U & (vlSelfRef.u_core__DOT__wacc 
                                         >> 0x10U)))
                            ? 0xffffU : (0xffffU & vlSelfRef.u_core__DOT__wacc));
                    vlSelfRef.u_core__DOT__resp_nak = 0U;
                    __Vdly__u_core__DOT__state = 0xdU;
                } else if (vlSelfRef.u_core__DOT__ev
                           [(3U & (IData)(vlSelfRef.u_core__DOT__eidx))]) {
                    vlSelfRef.u_core__DOT__hb_sel = 
                        (0xfU & ((IData)(1U) << (3U 
                                                 & (IData)(vlSelfRef.u_core__DOT__eidx))));
                    vlSelfRef.u_core__DOT__hb_cmd = 3U;
                    __Vdly__u_core__DOT__state = 0xbU;
                } else {
                    __Vdly__u_core__DOT__eidx = (7U 
                                                 & ((IData)(1U) 
                                                    + (IData)(vlSelfRef.u_core__DOT__eidx)));
                }
            } else if ((1U & (IData)(vlSelfRef.u_core__DOT__state))) {
                if (vlSelfRef.u_core__DOT__bound) {
                    if ((0U == (3U & (IData)(vlSelfRef.u_core__DOT__lr_a0)))) {
                        vlSelfRef.u_core__DOT__viewdat 
                            = vlSelfRef.u_core__DOT__act;
                        vlSelfRef.u_core__DOT__resp_nak = 0U;
                        __Vdly__u_core__DOT__state = 0xdU;
                    } else if ((1U == (3U & (IData)(vlSelfRef.u_core__DOT__lr_a0)))) {
                        __Vdly__u_core__DOT__wacc = 0U;
                        __Vdly__u_core__DOT__eidx = 0U;
                        __Vdly__u_core__DOT__state = 0xaU;
                    } else if ((2U == (3U & (IData)(vlSelfRef.u_core__DOT__lr_a0)))) {
                        vlSelfRef.u_core__DOT__df_rd = 1U;
                        vlSelfRef.u_core__DOT__df_addr 
                            = (0xfU & (IData)(vlSelfRef.u_core__DOT__lr_a1));
                        __Vdly__u_core__DOT__state = 0xcU;
                    } else {
                        vlSelfRef.u_core__DOT__resp_nak = 1U;
                        vlSelfRef.u_core__DOT__viewdat = 0U;
                        __Vdly__u_core__DOT__state = 0xdU;
                    }
                } else {
                    vlSelfRef.u_core__DOT__resp_nak = 1U;
                    vlSelfRef.u_core__DOT__viewdat = 0U;
                    __Vdly__u_core__DOT__state = 0xdU;
                }
            } else if (vlSelfRef.hb_done) {
                vlSelfRef.u_core__DOT__hb_cmd = 3U;
                __Vdly__u_core__DOT__state = 0x14U;
            }
        } else if ((4U & (IData)(vlSelfRef.u_core__DOT__state))) {
            if ((2U & (IData)(vlSelfRef.u_core__DOT__state))) {
                if ((1U & (IData)(vlSelfRef.u_core__DOT__state))) {
                    if ((4U == (IData)(vlSelfRef.u_core__DOT__eidx))) {
                        __Vdly__u_core__DOT__ci_ready 
                            = (1U & (~ ((IData)(vlSelfRef.s_tick) 
                                        | (IData)(vlSelfRef.u_core__DOT__tick_pend))));
                        __Vdly__u_core__DOT__state = 2U;
                    } else if ((vlSelfRef.u_core__DOT__ev
                                [(3U & (IData)(vlSelfRef.u_core__DOT__eidx))] 
                                & (vlSelfRef.u_core__DOT__etab
                                   [(3U & (IData)(vlSelfRef.u_core__DOT__eidx))] 
                                   == (IData)(vlSelfRef.u_core__DOT__lr_src)))) {
                        vlSelfRef.u_core__DOT__hb_sel 
                            = (0xfU & ((IData)(1U) 
                                       << (3U & (IData)(vlSelfRef.u_core__DOT__eidx))));
                        if (vlSelfRef.u_core__DOT__eg_live) {
                            vlSelfRef.u_core__DOT__hb_cmd = 5U;
                            vlSelfRef.u_core__DOT__hb_gcl 
                                = vlSelfRef.u_core__DOT__eg_gclass;
                            __Vdly__u_core__DOT__state = 8U;
                        } else {
                            vlSelfRef.u_core__DOT__hb_cmd = 3U;
                            __Vdly__u_core__DOT__state = 0x14U;
                        }
                    } else {
                        __Vdly__u_core__DOT__eidx = 
                            (7U & ((IData)(1U) + (IData)(vlSelfRef.u_core__DOT__eidx)));
                    }
                } else {
                    __Vdly__u_core__DOT__eidx = 0U;
                    __Vdly__u_core__DOT__state = 7U;
                }
            } else if ((1U & (IData)(vlSelfRef.u_core__DOT__state))) {
                if (vlSelfRef.hb_done) {
                    vlSelfRef.u_core__DOT__resp_nak = 0U;
                    vlSelfRef.u_core__DOT__viewdat = 0U;
                    __Vdly__u_core__DOT__state = 0xdU;
                }
            } else {
                __VdlyVal__u_core__DOT__etab__v0 = vlSelfRef.u_core__DOT__lr_src;
                __VdlyDim0__u_core__DOT__etab__v0 = 
                    (3U & (IData)(vlSelfRef.u_core__DOT__lr_a0));
                __VdlySet__u_core__DOT__etab__v0 = 1U;
                __VdlyDim0__u_core__DOT__ev__v0 = (3U 
                                                   & (IData)(vlSelfRef.u_core__DOT__lr_a0));
                vlSelfRef.u_core__DOT__hb_sel = (0xfU 
                                                 & ((IData)(1U) 
                                                    << 
                                                    (3U 
                                                     & (IData)(vlSelfRef.u_core__DOT__lr_a0))));
                vlSelfRef.u_core__DOT__hb_cmd = 4U;
                vlSelfRef.u_core__DOT__hb_base = vlSelfRef.u_core__DOT__lr_a1;
                __Vdly__u_core__DOT__state = 5U;
            }
        } else if ((2U & (IData)(vlSelfRef.u_core__DOT__state))) {
            if ((1U & (IData)(vlSelfRef.u_core__DOT__state))) {
                vlSelfRef.u_core__DOT__df_wr = 1U;
                vlSelfRef.u_core__DOT__df_addr = vlSelfRef.u_core__DOT__lr_a0;
                vlSelfRef.u_core__DOT__df_wdata = vlSelfRef.u_core__DOT__lr_a1;
                vlSelfRef.u_core__DOT__resp_nak = 0U;
                vlSelfRef.u_core__DOT__viewdat = 0U;
                __Vdly__u_core__DOT__state = 0xdU;
            } else if (vlSelfRef.u_core__DOT__tick_pend) {
                __Vdly__u_core__DOT__ci_ready = 0U;
                vlSelfRef.u_core__DOT__hb_sel = 0U;
                __Vdly__u_core__DOT__state = 0xeU;
            } else {
                __Vdly__u_core__DOT__ci_ready = (1U 
                                                 & (~ 
                                                    ((IData)(vlSelfRef.s_tick) 
                                                     | (IData)(vlSelfRef.u_core__DOT__tick_pend))));
                vlSelfRef.u_core__DOT__hb_sel = 0U;
                if (((IData)(vlSelfRef.ci_valid) & (IData)(vlSelfRef.u_core__DOT__ci_ready))) {
                    vlSelfRef.u_core__DOT__lr_src = vlSelfRef.ci_src;
                    vlSelfRef.u_core__DOT__lr_a0 = 
                        (0xfU & (IData)(vlSelfRef.ci_a0));
                    vlSelfRef.u_core__DOT__lr_a1 = vlSelfRef.ci_a1;
                    vlSelfRef.u_core__DOT__lr_a2 = vlSelfRef.ci_a2;
                    vlSelfRef.u_core__DOT__lr_dat = vlSelfRef.ci_dat;
                    __Vdly__u_core__DOT__ci_ready = 0U;
                    if ((4U & (IData)(vlSelfRef.ci_op))) {
                        if ((2U & (IData)(vlSelfRef.ci_op))) {
                            if ((1U & (IData)(vlSelfRef.ci_op))) {
                                vlSelfRef.u_core__DOT__resp_nak = 1U;
                                vlSelfRef.u_core__DOT__viewdat = 0U;
                                __Vdly__u_core__DOT__state = 0xdU;
                            } else {
                                __Vdly__u_core__DOT__state = 2U;
                            }
                        } else {
                            __Vdly__u_core__DOT__state = 2U;
                        }
                    } else {
                        __Vdly__u_core__DOT__state 
                            = ((2U & (IData)(vlSelfRef.ci_op))
                                ? ((1U & (IData)(vlSelfRef.ci_op))
                                    ? 9U : 6U) : ((1U 
                                                   & (IData)(vlSelfRef.ci_op))
                                                   ? 4U
                                                   : 3U));
                    }
                }
            }
        } else if ((1U & (IData)(vlSelfRef.u_core__DOT__state))) {
            __Vdly__u_core__DOT__ci_ready = 1U;
            if (((IData)(vlSelfRef.ci_valid) & (IData)(vlSelfRef.u_core__DOT__ci_ready))) {
                __Vdly__u_core__DOT__ci_ready = 0U;
                vlSelfRef.u_core__DOT__lr_src = vlSelfRef.ci_src;
                vlSelfRef.u_core__DOT__lr_a2 = vlSelfRef.ci_a2;
                if ((0U == (IData)(vlSelfRef.ci_op))) {
                    vlSelfRef.u_core__DOT__cell_id 
                        = (0xfU & (IData)(vlSelfRef.ci_a0));
                    vlSelfRef.u_core__DOT__bound = 1U;
                    vlSelfRef.u_core__DOT__resp_nak = 0U;
                } else {
                    vlSelfRef.u_core__DOT__resp_nak = 1U;
                }
                vlSelfRef.u_core__DOT__viewdat = 0U;
                __Vdly__u_core__DOT__state = 0xdU;
            }
        } else {
            __Vdly__u_core__DOT__state = 1U;
        }
    } else {
        __Vdly__u_core__DOT__tick_pend = 0U;
        __VdlySet__u_core__DOT__u_rq__DOT__R__v2 = 1U;
        __Vdly__u_egbuf__DOT__a_v = 0U;
        vlSelfRef.u_egbuf__DOT__b_v = 0U;
        vlSelfRef.u_egbuf__DOT__a_q[0U] = 0U;
        vlSelfRef.u_egbuf__DOT__a_q[1U] = 0U;
        vlSelfRef.u_egbuf__DOT__a_q[2U] = 0U;
        vlSelfRef.u_egbuf__DOT__b_q[0U] = 0U;
        vlSelfRef.u_egbuf__DOT__b_q[1U] = 0U;
        vlSelfRef.u_egbuf__DOT__b_q[2U] = 0U;
        __Vdly__u_inbuf__DOT__a_v = 0U;
        vlSelfRef.u_inbuf__DOT__b_v = 0U;
        vlSelfRef.u_inbuf__DOT__a_q[0U] = 0U;
        vlSelfRef.u_inbuf__DOT__a_q[1U] = 0U;
        vlSelfRef.u_inbuf__DOT__a_q[2U] = 0U;
        vlSelfRef.u_inbuf__DOT__b_q[0U] = 0U;
        vlSelfRef.u_inbuf__DOT__b_q[1U] = 0U;
        vlSelfRef.u_inbuf__DOT__b_q[2U] = 0U;
        vlSelfRef.u_core__DOT__u_eg__DOT__f = 0U;
        vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__j = 1U;
        vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__ridx = 0U;
        vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__acc = 0U;
        vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__o_done = 0U;
        vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__o_w = 0U;
        vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__o_ovf = 0U;
        __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v11 = 1U;
        vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__j = 2U;
        __Vdly__edges__BRA__1__KET____DOT__u_hebb__DOT__hl_cnt = 0U;
        __Vdly__edges__BRA__1__KET____DOT__u_hebb__DOT__wh = 0U;
        __Vdly__edges__BRA__1__KET____DOT__u_hebb__DOT__age = 0U;
        vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__base = 0U;
        vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__rstate = 0U;
        __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v12 = 1U;
        vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__j = 3U;
        __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v13 = 1U;
        vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__j = 4U;
        __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v14 = 1U;
        vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__j = 5U;
        __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v15 = 1U;
        vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__j = 6U;
        __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v16 = 1U;
        vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__j = 7U;
        __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v17 = 1U;
        vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__j = 8U;
        __VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v18 = 1U;
        vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__j = 1U;
        vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__ridx = 0U;
        vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__acc = 0U;
        vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__o_done = 0U;
        vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__o_w = 0U;
        vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__o_ovf = 0U;
        __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v11 = 1U;
        vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__j = 2U;
        __Vdly__edges__BRA__2__KET____DOT__u_hebb__DOT__hl_cnt = 0U;
        __Vdly__edges__BRA__2__KET____DOT__u_hebb__DOT__wh = 0U;
        __Vdly__edges__BRA__2__KET____DOT__u_hebb__DOT__age = 0U;
        vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__base = 0U;
        vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__rstate = 0U;
        __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v12 = 1U;
        vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__j = 3U;
        __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v13 = 1U;
        vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__j = 4U;
        __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v14 = 1U;
        vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__j = 5U;
        __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v15 = 1U;
        vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__j = 6U;
        __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v16 = 1U;
        vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__j = 7U;
        __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v17 = 1U;
        vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__j = 8U;
        __VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v18 = 1U;
        vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__j = 1U;
        vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__ridx = 0U;
        vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__acc = 0U;
        vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__o_done = 0U;
        vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__o_w = 0U;
        vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__o_ovf = 0U;
        __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v11 = 1U;
        vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__j = 2U;
        __Vdly__edges__BRA__3__KET____DOT__u_hebb__DOT__hl_cnt = 0U;
        __Vdly__edges__BRA__3__KET____DOT__u_hebb__DOT__wh = 0U;
        __Vdly__edges__BRA__3__KET____DOT__u_hebb__DOT__age = 0U;
        vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__base = 0U;
        vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__rstate = 0U;
        __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v12 = 1U;
        vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__j = 3U;
        __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v13 = 1U;
        vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__j = 4U;
        __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v14 = 1U;
        vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__j = 5U;
        __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v15 = 1U;
        vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__j = 6U;
        __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v16 = 1U;
        vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__j = 7U;
        __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v17 = 1U;
        vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__j = 8U;
        __VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v18 = 1U;
        vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__j = 1U;
        vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__ridx = 0U;
        vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__acc = 0U;
        vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__o_done = 0U;
        vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__o_w = 0U;
        vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__o_ovf = 0U;
        __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v11 = 1U;
        vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__j = 2U;
        __Vdly__edges__BRA__0__KET____DOT__u_hebb__DOT__hl_cnt = 0U;
        __Vdly__edges__BRA__0__KET____DOT__u_hebb__DOT__wh = 0U;
        __Vdly__edges__BRA__0__KET____DOT__u_hebb__DOT__age = 0U;
        vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__base = 0U;
        vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__rstate = 0U;
        __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v12 = 1U;
        vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__j = 3U;
        __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v13 = 1U;
        vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__j = 4U;
        __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v14 = 1U;
        vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__j = 5U;
        __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v15 = 1U;
        vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__j = 6U;
        __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v16 = 1U;
        vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__j = 7U;
        __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v17 = 1U;
        vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__j = 8U;
        __VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v18 = 1U;
        __Vdly__u_core__DOT__ci_ready = 0U;
        __Vdly__u_core__DOT__lo_valid = 0U;
        __Vdly__u_core__DOT__lx_valid = 0U;
        __Vdly__u_core__DOT__eidx = 0U;
        __Vdly__u_core__DOT__wacc = 0U;
        __Vdly__u_core__DOT__state = 0U;
        vlSelfRef.u_core__DOT__lo_op = 0U;
        vlSelfRef.u_core__DOT__lo_dst = 0U;
        vlSelfRef.u_core__DOT__lo_src = 0U;
        vlSelfRef.u_core__DOT__lo_a0 = 0U;
        vlSelfRef.u_core__DOT__lo_a1 = 0U;
        vlSelfRef.u_core__DOT__lo_a2 = 0U;
        vlSelfRef.u_core__DOT__lo_dat = 0U;
        vlSelfRef.u_core__DOT__lx_op = 0U;
        vlSelfRef.u_core__DOT__lx_dst = 0U;
        vlSelfRef.u_core__DOT__lx_src = 0U;
        vlSelfRef.u_core__DOT__lx_a0 = 0U;
        vlSelfRef.u_core__DOT__lx_a1 = 0U;
        vlSelfRef.u_core__DOT__lx_a2 = 0U;
        vlSelfRef.u_core__DOT__lx_dat = 0U;
        vlSelfRef.u_core__DOT__hb_cmd = 0U;
        vlSelfRef.u_core__DOT__hb_sel = 0U;
        vlSelfRef.u_core__DOT__hb_base = 0U;
        vlSelfRef.u_core__DOT__hb_gcl = 0U;
        vlSelfRef.u_core__DOT__eg_fire = 0U;
        vlSelfRef.u_core__DOT__df_wr = 0U;
        vlSelfRef.u_core__DOT__df_addr = 0U;
        vlSelfRef.u_core__DOT__df_wdata = 0U;
        vlSelfRef.u_core__DOT__df_rd = 0U;
        vlSelfRef.u_core__DOT__bound = 0U;
        vlSelfRef.u_core__DOT__cell_id = 0U;
        __Vdly__u_core__DOT__act = 0U;
        __Vdly__u_core__DOT__refr = 0U;
        vlSelfRef.u_core__DOT__viewdat = 0U;
        vlSelfRef.u_core__DOT__resp_nak = 0U;
        vlSelfRef.u_core__DOT__afire = 0U;
        vlSelfRef.u_core__DOT__lr_src = 0U;
        vlSelfRef.u_core__DOT__lr_a0 = 0U;
        vlSelfRef.u_core__DOT__lr_a1 = 0U;
        vlSelfRef.u_core__DOT__lr_a2 = 0U;
        vlSelfRef.u_core__DOT__lr_dat = 0U;
        vlSelfRef.u_core__DOT__eff_w = 0U;
        vlSelfRef.u_core__DOT__eff_p = 0ULL;
        __VdlySet__u_core__DOT__etab__v1 = 1U;
    }
    if (vlSelfRef.i_por_n) {
        if (((IData)(vlSelfRef.df_wr_g) & (0xdU != (IData)(vlSelfRef.df_addr_g)))) {
            __VdlyVal__u_df__DOT__dial__v0 = vlSelfRef.df_wdata_g;
            __VdlyDim0__u_df__DOT__dial__v0 = vlSelfRef.df_addr_g;
            __VdlySet__u_df__DOT__dial__v0 = 1U;
        }
        if (vlSelfRef.df_rd) {
            vlSelfRef.u_df__DOT__o_rdata = ((0xdU == (IData)(vlSelfRef.df_addr_g))
                                             ? (IData)(vlSelfRef.w_ftrace)
                                             : vlSelfRef.u_df__DOT__dial
                                            [vlSelfRef.df_addr_g]);
        }
    } else {
        __VdlySet__u_df__DOT__dial__v1 = 1U;
        vlSelfRef.u_df__DOT__o_rdata = 0U;
    }
    vlSelfRef.u_df__DOT__o_rstb = ((IData)(vlSelfRef.i_por_n) 
                                   && (IData)(vlSelfRef.df_rd));
    if (__VdlySet__u_core__DOT__u_rq__DOT__R__v0) {
        vlSelfRef.u_core__DOT__u_rq__DOT__R[__VdlyDim0__u_core__DOT__u_rq__DOT__R__v0] 
            = __VdlyVal__u_core__DOT__u_rq__DOT__R__v0;
    }
    if (__VdlySet__u_core__DOT__u_rq__DOT__R__v1) {
        vlSelfRef.u_core__DOT__u_rq__DOT__R[__VdlyDim0__u_core__DOT__u_rq__DOT__R__v1] 
            = __VdlyVal__u_core__DOT__u_rq__DOT__R__v1;
    }
    if (__VdlySet__u_core__DOT__u_rq__DOT__R__v2) {
        vlSelfRef.u_core__DOT__u_rq__DOT__R[0U] = 0U;
        vlSelfRef.u_core__DOT__u_rq__DOT__R[1U] = 0U;
        vlSelfRef.u_core__DOT__u_rq__DOT__R[2U] = 0U;
        vlSelfRef.u_core__DOT__u_rq__DOT__R[3U] = 0U;
    }
    if (__VdlySet__u_df__DOT__dial__v0) {
        vlSelfRef.u_df__DOT__dial[__VdlyDim0__u_df__DOT__dial__v0] 
            = __VdlyVal__u_df__DOT__dial__v0;
    }
    if (__VdlySet__u_df__DOT__dial__v1) {
        vlSelfRef.u_df__DOT__dial[0U] = 0x800U;
        vlSelfRef.u_df__DOT__dial[1U] = 0x80U;
        vlSelfRef.u_df__DOT__dial[2U] = 6U;
        vlSelfRef.u_df__DOT__dial[3U] = 0xcU;
        vlSelfRef.u_df__DOT__dial[4U] = 5U;
        vlSelfRef.u_df__DOT__dial[5U] = 0x6000U;
        vlSelfRef.u_df__DOT__dial[6U] = 4U;
        vlSelfRef.u_df__DOT__dial[7U] = 0x2ccdU;
        vlSelfRef.u_df__DOT__dial[8U] = 0x14U;
        vlSelfRef.u_df__DOT__dial[9U] = 0U;
        vlSelfRef.u_df__DOT__dial[0xaU] = 0x40U;
        vlSelfRef.u_df__DOT__dial[0xbU] = 2U;
        vlSelfRef.u_df__DOT__dial[0xcU] = 0U;
        vlSelfRef.u_df__DOT__dial[0xdU] = 0U;
        vlSelfRef.u_df__DOT__dial[0xeU] = 8U;
        vlSelfRef.u_df__DOT__dial[0xfU] = 8U;
    }
    vlSelfRef.u_egbuf__DOT__a_v = __Vdly__u_egbuf__DOT__a_v;
    vlSelfRef.u_inbuf__DOT__a_v = __Vdly__u_inbuf__DOT__a_v;
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__hl_cnt 
        = __Vdly__edges__BRA__1__KET____DOT__u_hebb__DOT__hl_cnt;
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__age 
        = __Vdly__edges__BRA__1__KET____DOT__u_hebb__DOT__age;
    if (__VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v0) {
        vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__c[7U] 
            = __VdlyVal__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v0;
    }
    if (__VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v1) {
        vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__c[__VdlyDim0__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v1] 
            = __VdlyVal__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v1;
    }
    if (__VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v2) {
        vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__c[7U] 
            = __VdlyVal__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v2;
    }
    if (__VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v3) {
        vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__c[6U] 
            = __VdlyVal__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v3;
    }
    if (__VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v4) {
        vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__c[5U] 
            = __VdlyVal__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v4;
    }
    if (__VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v5) {
        vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__c[4U] 
            = __VdlyVal__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v5;
    }
    if (__VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v6) {
        vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__c[3U] 
            = __VdlyVal__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v6;
    }
    if (__VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v7) {
        vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__c[2U] 
            = __VdlyVal__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v7;
    }
    if (__VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v8) {
        vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__c[1U] 
            = __VdlyVal__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v8;
        vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__c[0U] = 0U;
    }
    if (__VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v10) {
        vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__c[0U] 
            = __VdlyVal__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v10;
    }
    if (__VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v11) {
        vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__c[0U] = 0U;
    }
    if (__VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v12) {
        vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__c[1U] = 0U;
    }
    if (__VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v13) {
        vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__c[2U] = 0U;
    }
    if (__VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v14) {
        vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__c[3U] = 0U;
    }
    if (__VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v15) {
        vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__c[4U] = 0U;
    }
    if (__VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v16) {
        vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__c[5U] = 0U;
    }
    if (__VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v17) {
        vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__c[6U] = 0U;
    }
    if (__VdlySet__edges__BRA__1__KET____DOT__u_hebb__DOT__c__v18) {
        vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__c[7U] = 0U;
    }
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__wh 
        = __Vdly__edges__BRA__1__KET____DOT__u_hebb__DOT__wh;
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__hl_cnt 
        = __Vdly__edges__BRA__2__KET____DOT__u_hebb__DOT__hl_cnt;
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__age 
        = __Vdly__edges__BRA__2__KET____DOT__u_hebb__DOT__age;
    if (__VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v0) {
        vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__c[7U] 
            = __VdlyVal__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v0;
    }
    if (__VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v1) {
        vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__c[__VdlyDim0__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v1] 
            = __VdlyVal__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v1;
    }
    if (__VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v2) {
        vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__c[7U] 
            = __VdlyVal__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v2;
    }
    if (__VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v3) {
        vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__c[6U] 
            = __VdlyVal__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v3;
    }
    if (__VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v4) {
        vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__c[5U] 
            = __VdlyVal__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v4;
    }
    if (__VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v5) {
        vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__c[4U] 
            = __VdlyVal__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v5;
    }
    if (__VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v6) {
        vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__c[3U] 
            = __VdlyVal__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v6;
    }
    if (__VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v7) {
        vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__c[2U] 
            = __VdlyVal__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v7;
    }
    if (__VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v8) {
        vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__c[1U] 
            = __VdlyVal__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v8;
        vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__c[0U] = 0U;
    }
    if (__VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v10) {
        vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__c[0U] 
            = __VdlyVal__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v10;
    }
    if (__VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v11) {
        vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__c[0U] = 0U;
    }
    if (__VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v12) {
        vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__c[1U] = 0U;
    }
    if (__VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v13) {
        vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__c[2U] = 0U;
    }
    if (__VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v14) {
        vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__c[3U] = 0U;
    }
    if (__VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v15) {
        vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__c[4U] = 0U;
    }
    if (__VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v16) {
        vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__c[5U] = 0U;
    }
    if (__VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v17) {
        vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__c[6U] = 0U;
    }
    if (__VdlySet__edges__BRA__2__KET____DOT__u_hebb__DOT__c__v18) {
        vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__c[7U] = 0U;
    }
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__wh 
        = __Vdly__edges__BRA__2__KET____DOT__u_hebb__DOT__wh;
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__hl_cnt 
        = __Vdly__edges__BRA__3__KET____DOT__u_hebb__DOT__hl_cnt;
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__age 
        = __Vdly__edges__BRA__3__KET____DOT__u_hebb__DOT__age;
    if (__VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v0) {
        vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__c[7U] 
            = __VdlyVal__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v0;
    }
    if (__VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v1) {
        vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__c[__VdlyDim0__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v1] 
            = __VdlyVal__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v1;
    }
    if (__VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v2) {
        vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__c[7U] 
            = __VdlyVal__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v2;
    }
    if (__VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v3) {
        vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__c[6U] 
            = __VdlyVal__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v3;
    }
    if (__VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v4) {
        vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__c[5U] 
            = __VdlyVal__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v4;
    }
    if (__VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v5) {
        vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__c[4U] 
            = __VdlyVal__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v5;
    }
    if (__VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v6) {
        vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__c[3U] 
            = __VdlyVal__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v6;
    }
    if (__VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v7) {
        vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__c[2U] 
            = __VdlyVal__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v7;
    }
    if (__VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v8) {
        vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__c[1U] 
            = __VdlyVal__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v8;
        vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__c[0U] = 0U;
    }
    if (__VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v10) {
        vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__c[0U] 
            = __VdlyVal__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v10;
    }
    if (__VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v11) {
        vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__c[0U] = 0U;
    }
    if (__VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v12) {
        vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__c[1U] = 0U;
    }
    if (__VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v13) {
        vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__c[2U] = 0U;
    }
    if (__VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v14) {
        vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__c[3U] = 0U;
    }
    if (__VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v15) {
        vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__c[4U] = 0U;
    }
    if (__VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v16) {
        vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__c[5U] = 0U;
    }
    if (__VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v17) {
        vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__c[6U] = 0U;
    }
    if (__VdlySet__edges__BRA__3__KET____DOT__u_hebb__DOT__c__v18) {
        vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__c[7U] = 0U;
    }
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__wh 
        = __Vdly__edges__BRA__3__KET____DOT__u_hebb__DOT__wh;
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__hl_cnt 
        = __Vdly__edges__BRA__0__KET____DOT__u_hebb__DOT__hl_cnt;
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__age 
        = __Vdly__edges__BRA__0__KET____DOT__u_hebb__DOT__age;
    if (__VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v0) {
        vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__c[7U] 
            = __VdlyVal__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v0;
    }
    if (__VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v1) {
        vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__c[__VdlyDim0__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v1] 
            = __VdlyVal__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v1;
    }
    if (__VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v2) {
        vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__c[7U] 
            = __VdlyVal__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v2;
    }
    if (__VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v3) {
        vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__c[6U] 
            = __VdlyVal__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v3;
    }
    if (__VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v4) {
        vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__c[5U] 
            = __VdlyVal__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v4;
    }
    if (__VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v5) {
        vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__c[4U] 
            = __VdlyVal__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v5;
    }
    if (__VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v6) {
        vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__c[3U] 
            = __VdlyVal__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v6;
    }
    if (__VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v7) {
        vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__c[2U] 
            = __VdlyVal__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v7;
    }
    if (__VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v8) {
        vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__c[1U] 
            = __VdlyVal__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v8;
        vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__c[0U] = 0U;
    }
    if (__VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v10) {
        vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__c[0U] 
            = __VdlyVal__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v10;
    }
    if (__VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v11) {
        vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__c[0U] = 0U;
    }
    if (__VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v12) {
        vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__c[1U] = 0U;
    }
    if (__VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v13) {
        vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__c[2U] = 0U;
    }
    if (__VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v14) {
        vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__c[3U] = 0U;
    }
    if (__VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v15) {
        vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__c[4U] = 0U;
    }
    if (__VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v16) {
        vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__c[5U] = 0U;
    }
    if (__VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v17) {
        vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__c[6U] = 0U;
    }
    if (__VdlySet__edges__BRA__0__KET____DOT__u_hebb__DOT__c__v18) {
        vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__c[7U] = 0U;
    }
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__wh 
        = __Vdly__edges__BRA__0__KET____DOT__u_hebb__DOT__wh;
    vlSelfRef.u_df__DOT__o_eta_f = vlSelfRef.u_df__DOT__dial
        [0U];
    vlSelfRef.d_eta_f = vlSelfRef.u_df__DOT__dial[0U];
    vlSelfRef.u_df__DOT__o_eta_s = vlSelfRef.u_df__DOT__dial
        [1U];
    vlSelfRef.d_eta_s = vlSelfRef.u_df__DOT__dial[1U];
    vlSelfRef.u_df__DOT__o_thresh = vlSelfRef.u_df__DOT__dial
        [5U];
    vlSelfRef.u_df__DOT__o_refr = vlSelfRef.u_df__DOT__dial
        [6U];
    vlSelfRef.u_df__DOT__o_cosmin = vlSelfRef.u_df__DOT__dial
        [7U];
    vlSelfRef.d_cosmin = vlSelfRef.u_df__DOT__dial[7U];
    vlSelfRef.u_df__DOT__o_hl = vlSelfRef.u_df__DOT__dial
        [0xaU];
    vlSelfRef.u_df__DOT__o_floor = vlSelfRef.u_df__DOT__dial
        [0xcU];
    vlSelfRef.u_df__DOT__o_kf = (0xfU & vlSelfRef.u_df__DOT__dial
                                 [2U]);
    vlSelfRef.u_df__DOT__o_ks = (0xfU & vlSelfRef.u_df__DOT__dial
                                 [3U]);
    vlSelfRef.d_ka = (0xfU & vlSelfRef.u_df__DOT__dial
                      [4U]);
    vlSelfRef.d_hl = vlSelfRef.u_df__DOT__dial[0xaU];
    vlSelfRef.d_kle = (0xfU & vlSelfRef.u_df__DOT__dial
                       [0xbU]);
    vlSelfRef.d_floor = vlSelfRef.u_df__DOT__dial[0xcU];
    vlSelfRef.d_qleak = (0xfU & vlSelfRef.u_df__DOT__dial
                         [0xfU]);
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__hlth 
        = vlSelfRef.u_df__DOT__dial[0xaU];
    vlSelfRef.d_rqen = (1U & (vlSelfRef.u_df__DOT__dial
                              [0xeU] >> 0xfU));
    vlSelfRef.d_mode = (1U & vlSelfRef.u_df__DOT__dial
                        [9U]);
    vlSelfRef.d_p0e = (0x1fU & vlSelfRef.u_df__DOT__dial
                       [8U]);
    vlSelfRef.d_qdw = (0xfU & vlSelfRef.u_df__DOT__dial
                       [0xeU]);
    vlSelfRef.u_egbuf__DOT__s_ready = (1U & (~ (IData)(vlSelfRef.u_egbuf__DOT__b_v)));
    vlSelfRef.u_egbuf__DOT__m_valid = vlSelfRef.u_egbuf__DOT__a_v;
    vlSelfRef.li_valid_w = vlSelfRef.u_egbuf__DOT__a_v;
    vlSelfRef.li_op_w = (7U & (vlSelfRef.u_egbuf__DOT__a_q[2U] 
                               >> 8U));
    vlSelfRef.li_src_w = (0xfU & (vlSelfRef.u_egbuf__DOT__a_q[2U] 
                                  >> 4U));
    vlSelfRef.li_dst_w = (0xfU & vlSelfRef.u_egbuf__DOT__a_q[2U]);
    vlSelfRef.li_a0_w = (vlSelfRef.u_egbuf__DOT__a_q[1U] 
                         >> 0x10U);
    vlSelfRef.li_a1_w = (0xffffU & vlSelfRef.u_egbuf__DOT__a_q[1U]);
    vlSelfRef.li_a2_w = (vlSelfRef.u_egbuf__DOT__a_q[0U] 
                         >> 0x10U);
    vlSelfRef.li_dat_w = (0xffffU & vlSelfRef.u_egbuf__DOT__a_q[0U]);
    vlSelfRef.u_inbuf__DOT__m_valid = vlSelfRef.u_inbuf__DOT__a_v;
    vlSelfRef.u_core__DOT__ci_a0_rsvd = (vlSelfRef.u_inbuf__DOT__a_q[1U] 
                                         >> 0x14U);
    vlSelfRef.u_inbuf__DOT__m_dst = (0xfU & vlSelfRef.u_inbuf__DOT__a_q[2U]);
    vlSelfRef.ld_ready = (1U & (~ (IData)(vlSelfRef.u_inbuf__DOT__b_v)));
    vlSelfRef.u_core__DOT__o_ftrace = vlSelfRef.u_core__DOT__u_eg__DOT__f;
    vlSelfRef.u_core__DOT__u_eg__DOT__o_f = vlSelfRef.u_core__DOT__u_eg__DOT__f;
    vlSelfRef.w_ftrace = vlSelfRef.u_core__DOT__u_eg__DOT__f;
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__hlc 
        = (0x1ffffU & ((IData)(1U) + (IData)(vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__hl_cnt)));
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__agen 
        = ((IData)(1U) + vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__age);
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__ridx32 
        = vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__ridx;
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__g_lad_sat__DOT__sat 
        = (1U & (vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__acc 
                 >> 0x10U));
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__whs 
        = ((0xffU < (IData)(vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__wh))
            ? 0xffffU : (0xffffU & VL_SHIFTL_III(16,16,32, (IData)(vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__wh), 8U)));
    __Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__39__v 
        = vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__wh;
    __Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__39__Vfuncout = 0U;
    if ((1U & (IData)(__Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__39__v))) {
        __Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__39__Vfuncout = 0U;
    }
    if ((2U & (IData)(__Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__39__v))) {
        __Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__39__Vfuncout = 1U;
    }
    if ((4U & (IData)(__Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__39__v))) {
        __Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__39__Vfuncout = 2U;
    }
    if ((8U & (IData)(__Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__39__v))) {
        __Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__39__Vfuncout = 3U;
    }
    if ((0x10U & (IData)(__Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__39__v))) {
        __Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__39__Vfuncout = 4U;
    }
    if ((0x20U & (IData)(__Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__39__v))) {
        __Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__39__Vfuncout = 5U;
    }
    if ((0x40U & (IData)(__Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__39__v))) {
        __Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__39__Vfuncout = 6U;
    }
    if ((0x80U & (IData)(__Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__39__v))) {
        __Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__39__Vfuncout = 7U;
    }
    if ((0x100U & (IData)(__Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__39__v))) {
        __Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__39__Vfuncout = 8U;
    }
    if ((0x200U & (IData)(__Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__39__v))) {
        __Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__39__Vfuncout = 9U;
    }
    if ((0x400U & (IData)(__Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__39__v))) {
        __Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__39__Vfuncout = 0xaU;
    }
    if ((0x800U & (IData)(__Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__39__v))) {
        __Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__39__Vfuncout = 0xbU;
    }
    if ((0x1000U & (IData)(__Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__39__v))) {
        __Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__39__Vfuncout = 0xcU;
    }
    if ((0x2000U & (IData)(__Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__39__v))) {
        __Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__39__Vfuncout = 0xdU;
    }
    if ((0x4000U & (IData)(__Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__39__v))) {
        __Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__39__Vfuncout = 0xeU;
    }
    if ((0x8000U & (IData)(__Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__39__v))) {
        __Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__39__Vfuncout = 0xfU;
    }
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__wmsb 
        = __Vfunc_edges__BRA__1__KET____DOT__u_hebb__DOT__msb16__39__Vfuncout;
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__hlc 
        = (0x1ffffU & ((IData)(1U) + (IData)(vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__hl_cnt)));
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__agen 
        = ((IData)(1U) + vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__age);
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__ridx32 
        = vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__ridx;
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__g_lad_sat__DOT__sat 
        = (1U & (vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__acc 
                 >> 0x10U));
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__whs 
        = ((0xffU < (IData)(vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__wh))
            ? 0xffffU : (0xffffU & VL_SHIFTL_III(16,16,32, (IData)(vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__wh), 8U)));
    __Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__40__v 
        = vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__wh;
    __Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__40__Vfuncout = 0U;
    if ((1U & (IData)(__Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__40__v))) {
        __Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__40__Vfuncout = 0U;
    }
    if ((2U & (IData)(__Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__40__v))) {
        __Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__40__Vfuncout = 1U;
    }
    if ((4U & (IData)(__Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__40__v))) {
        __Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__40__Vfuncout = 2U;
    }
    if ((8U & (IData)(__Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__40__v))) {
        __Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__40__Vfuncout = 3U;
    }
    if ((0x10U & (IData)(__Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__40__v))) {
        __Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__40__Vfuncout = 4U;
    }
    if ((0x20U & (IData)(__Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__40__v))) {
        __Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__40__Vfuncout = 5U;
    }
    if ((0x40U & (IData)(__Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__40__v))) {
        __Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__40__Vfuncout = 6U;
    }
    if ((0x80U & (IData)(__Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__40__v))) {
        __Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__40__Vfuncout = 7U;
    }
    if ((0x100U & (IData)(__Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__40__v))) {
        __Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__40__Vfuncout = 8U;
    }
    if ((0x200U & (IData)(__Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__40__v))) {
        __Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__40__Vfuncout = 9U;
    }
    if ((0x400U & (IData)(__Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__40__v))) {
        __Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__40__Vfuncout = 0xaU;
    }
    if ((0x800U & (IData)(__Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__40__v))) {
        __Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__40__Vfuncout = 0xbU;
    }
    if ((0x1000U & (IData)(__Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__40__v))) {
        __Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__40__Vfuncout = 0xcU;
    }
    if ((0x2000U & (IData)(__Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__40__v))) {
        __Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__40__Vfuncout = 0xdU;
    }
    if ((0x4000U & (IData)(__Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__40__v))) {
        __Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__40__Vfuncout = 0xeU;
    }
    if ((0x8000U & (IData)(__Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__40__v))) {
        __Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__40__Vfuncout = 0xfU;
    }
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__wmsb 
        = __Vfunc_edges__BRA__2__KET____DOT__u_hebb__DOT__msb16__40__Vfuncout;
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__hlc 
        = (0x1ffffU & ((IData)(1U) + (IData)(vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__hl_cnt)));
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__agen 
        = ((IData)(1U) + vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__age);
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__ridx32 
        = vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__ridx;
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__g_lad_sat__DOT__sat 
        = (1U & (vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__acc 
                 >> 0x10U));
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__whs 
        = ((0xffU < (IData)(vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__wh))
            ? 0xffffU : (0xffffU & VL_SHIFTL_III(16,16,32, (IData)(vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__wh), 8U)));
    __Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__41__v 
        = vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__wh;
    __Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__41__Vfuncout = 0U;
    if ((1U & (IData)(__Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__41__v))) {
        __Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__41__Vfuncout = 0U;
    }
    if ((2U & (IData)(__Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__41__v))) {
        __Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__41__Vfuncout = 1U;
    }
    if ((4U & (IData)(__Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__41__v))) {
        __Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__41__Vfuncout = 2U;
    }
    if ((8U & (IData)(__Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__41__v))) {
        __Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__41__Vfuncout = 3U;
    }
    if ((0x10U & (IData)(__Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__41__v))) {
        __Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__41__Vfuncout = 4U;
    }
    if ((0x20U & (IData)(__Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__41__v))) {
        __Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__41__Vfuncout = 5U;
    }
    if ((0x40U & (IData)(__Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__41__v))) {
        __Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__41__Vfuncout = 6U;
    }
    if ((0x80U & (IData)(__Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__41__v))) {
        __Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__41__Vfuncout = 7U;
    }
    if ((0x100U & (IData)(__Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__41__v))) {
        __Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__41__Vfuncout = 8U;
    }
    if ((0x200U & (IData)(__Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__41__v))) {
        __Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__41__Vfuncout = 9U;
    }
    if ((0x400U & (IData)(__Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__41__v))) {
        __Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__41__Vfuncout = 0xaU;
    }
    if ((0x800U & (IData)(__Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__41__v))) {
        __Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__41__Vfuncout = 0xbU;
    }
    if ((0x1000U & (IData)(__Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__41__v))) {
        __Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__41__Vfuncout = 0xcU;
    }
    if ((0x2000U & (IData)(__Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__41__v))) {
        __Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__41__Vfuncout = 0xdU;
    }
    if ((0x4000U & (IData)(__Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__41__v))) {
        __Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__41__Vfuncout = 0xeU;
    }
    if ((0x8000U & (IData)(__Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__41__v))) {
        __Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__41__Vfuncout = 0xfU;
    }
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__wmsb 
        = __Vfunc_edges__BRA__3__KET____DOT__u_hebb__DOT__msb16__41__Vfuncout;
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__hlc 
        = (0x1ffffU & ((IData)(1U) + (IData)(vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__hl_cnt)));
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__agen 
        = ((IData)(1U) + vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__age);
    vlSelfRef.done_vec = (((IData)(vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__o_done) 
                           << 3U) | (((IData)(vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__o_done) 
                                      << 2U) | (((IData)(vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__o_done) 
                                                 << 1U) 
                                                | (IData)(vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__o_done))));
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__ridx32 
        = vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__ridx;
    vlSelfRef.ovf_vec = (((IData)(vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__o_ovf) 
                          << 3U) | (((IData)(vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__o_ovf) 
                                     << 2U) | (((IData)(vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__o_ovf) 
                                                << 1U) 
                                               | (IData)(vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__o_ovf))));
    vlSelfRef.w_flat = (((QData)((IData)(vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__o_w)) 
                         << 0x30U) | (((QData)((IData)(
                                                       (((IData)(vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__o_w) 
                                                         << 0x10U) 
                                                        | (IData)(vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__o_w)))) 
                                       << 0x10U) | (QData)((IData)(vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__o_w))));
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__g_lad_sat__DOT__sat 
        = (1U & (vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__acc 
                 >> 0x10U));
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__whs 
        = ((0xffU < (IData)(vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__wh))
            ? 0xffffU : (0xffffU & VL_SHIFTL_III(16,16,32, (IData)(vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__wh), 8U)));
    __Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__38__v 
        = vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__wh;
    __Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__38__Vfuncout = 0U;
    if ((1U & (IData)(__Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__38__v))) {
        __Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__38__Vfuncout = 0U;
    }
    if ((2U & (IData)(__Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__38__v))) {
        __Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__38__Vfuncout = 1U;
    }
    if ((4U & (IData)(__Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__38__v))) {
        __Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__38__Vfuncout = 2U;
    }
    if ((8U & (IData)(__Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__38__v))) {
        __Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__38__Vfuncout = 3U;
    }
    if ((0x10U & (IData)(__Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__38__v))) {
        __Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__38__Vfuncout = 4U;
    }
    if ((0x20U & (IData)(__Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__38__v))) {
        __Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__38__Vfuncout = 5U;
    }
    if ((0x40U & (IData)(__Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__38__v))) {
        __Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__38__Vfuncout = 6U;
    }
    if ((0x80U & (IData)(__Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__38__v))) {
        __Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__38__Vfuncout = 7U;
    }
    if ((0x100U & (IData)(__Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__38__v))) {
        __Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__38__Vfuncout = 8U;
    }
    if ((0x200U & (IData)(__Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__38__v))) {
        __Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__38__Vfuncout = 9U;
    }
    if ((0x400U & (IData)(__Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__38__v))) {
        __Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__38__Vfuncout = 0xaU;
    }
    if ((0x800U & (IData)(__Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__38__v))) {
        __Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__38__Vfuncout = 0xbU;
    }
    if ((0x1000U & (IData)(__Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__38__v))) {
        __Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__38__Vfuncout = 0xcU;
    }
    if ((0x2000U & (IData)(__Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__38__v))) {
        __Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__38__Vfuncout = 0xdU;
    }
    if ((0x4000U & (IData)(__Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__38__v))) {
        __Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__38__Vfuncout = 0xeU;
    }
    if ((0x8000U & (IData)(__Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__38__v))) {
        __Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__38__Vfuncout = 0xfU;
    }
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__wmsb 
        = __Vfunc_edges__BRA__0__KET____DOT__u_hebb__DOT__msb16__38__Vfuncout;
    vlSelfRef.d_kf = vlSelfRef.u_df__DOT__o_kf;
    vlSelfRef.d_ks = vlSelfRef.u_df__DOT__o_ks;
    vlSelfRef.u_core__DOT__d_ka = vlSelfRef.d_ka;
    vlSelfRef.u_df__DOT__o_ka = vlSelfRef.d_ka;
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__i_hl 
        = vlSelfRef.d_hl;
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__i_hl 
        = vlSelfRef.d_hl;
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__i_hl 
        = vlSelfRef.d_hl;
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__i_hl 
        = vlSelfRef.d_hl;
    vlSelfRef.u_df__DOT__o_kle = vlSelfRef.d_kle;
    vlSelfRef.u_core__DOT__d_kle = vlSelfRef.d_kle;
    vlSelfRef.u_core__DOT__u_eg__DOT__fleak = (0xffffU 
                                               & ((IData)(vlSelfRef.u_core__DOT__u_eg__DOT__f) 
                                                  - 
                                                  ((IData)(vlSelfRef.u_core__DOT__u_eg__DOT__f) 
                                                   >> (IData)(vlSelfRef.d_kle))));
    vlSelfRef.u_core__DOT__d_floor = vlSelfRef.d_floor;
    vlSelfRef.u_core__DOT__u_eg__DOT__o_gclass = ((
                                                   (0U 
                                                    == (IData)(vlSelfRef.d_floor)) 
                                                   | (0U 
                                                      == (IData)(vlSelfRef.u_core__DOT__u_eg__DOT__f)))
                                                   ? 0U
                                                   : 
                                                  (0xfU 
                                                   & ((IData)(0xfU) 
                                                      - 
                                                      ([&]() {
                        vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__37__v 
                            = vlSelfRef.u_core__DOT__u_eg__DOT__f;
                        vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__37__Vfuncout = 0U;
                        if ((1U & (IData)(vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__37__v))) {
                            vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__37__Vfuncout = 0U;
                        }
                        vlSelfRef.u_core__DOT__u_eg__DOT__msb_idx__Vstatic__j = 1U;
                        if ((2U & (IData)(vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__37__v))) {
                            vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__37__Vfuncout = 1U;
                        }
                        vlSelfRef.u_core__DOT__u_eg__DOT__msb_idx__Vstatic__j = 2U;
                        if ((4U & (IData)(vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__37__v))) {
                            vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__37__Vfuncout = 2U;
                        }
                        vlSelfRef.u_core__DOT__u_eg__DOT__msb_idx__Vstatic__j = 3U;
                        if ((8U & (IData)(vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__37__v))) {
                            vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__37__Vfuncout = 3U;
                        }
                        vlSelfRef.u_core__DOT__u_eg__DOT__msb_idx__Vstatic__j = 4U;
                        if ((0x10U & (IData)(vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__37__v))) {
                            vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__37__Vfuncout = 4U;
                        }
                        vlSelfRef.u_core__DOT__u_eg__DOT__msb_idx__Vstatic__j = 5U;
                        if ((0x20U & (IData)(vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__37__v))) {
                            vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__37__Vfuncout = 5U;
                        }
                        vlSelfRef.u_core__DOT__u_eg__DOT__msb_idx__Vstatic__j = 6U;
                        if ((0x40U & (IData)(vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__37__v))) {
                            vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__37__Vfuncout = 6U;
                        }
                        vlSelfRef.u_core__DOT__u_eg__DOT__msb_idx__Vstatic__j = 7U;
                        if ((0x80U & (IData)(vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__37__v))) {
                            vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__37__Vfuncout = 7U;
                        }
                        vlSelfRef.u_core__DOT__u_eg__DOT__msb_idx__Vstatic__j = 8U;
                        if ((0x100U & (IData)(vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__37__v))) {
                            vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__37__Vfuncout = 8U;
                        }
                        vlSelfRef.u_core__DOT__u_eg__DOT__msb_idx__Vstatic__j = 9U;
                        if ((0x200U & (IData)(vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__37__v))) {
                            vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__37__Vfuncout = 9U;
                        }
                        vlSelfRef.u_core__DOT__u_eg__DOT__msb_idx__Vstatic__j = 0xaU;
                        if ((0x400U & (IData)(vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__37__v))) {
                            vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__37__Vfuncout = 0xaU;
                        }
                        vlSelfRef.u_core__DOT__u_eg__DOT__msb_idx__Vstatic__j = 0xbU;
                        if ((0x800U & (IData)(vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__37__v))) {
                            vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__37__Vfuncout = 0xbU;
                        }
                        vlSelfRef.u_core__DOT__u_eg__DOT__msb_idx__Vstatic__j = 0xcU;
                        if ((0x1000U & (IData)(vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__37__v))) {
                            vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__37__Vfuncout = 0xcU;
                        }
                        vlSelfRef.u_core__DOT__u_eg__DOT__msb_idx__Vstatic__j = 0xdU;
                        if ((0x2000U & (IData)(vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__37__v))) {
                            vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__37__Vfuncout = 0xdU;
                        }
                        vlSelfRef.u_core__DOT__u_eg__DOT__msb_idx__Vstatic__j = 0xeU;
                        if ((0x4000U & (IData)(vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__37__v))) {
                            vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__37__Vfuncout = 0xeU;
                        }
                        vlSelfRef.u_core__DOT__u_eg__DOT__msb_idx__Vstatic__j = 0xfU;
                        if ((0x8000U & (IData)(vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__37__v))) {
                            vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__37__Vfuncout = 0xfU;
                        }
                        vlSelfRef.u_core__DOT__u_eg__DOT__msb_idx__Vstatic__j = 0x10U;
                    }(), (IData)(vlSelfRef.__Vfunc_u_core__DOT__u_eg__DOT__msb_idx__37__Vfuncout)))));
    vlSelfRef.u_df__DOT__o_qleak = vlSelfRef.d_qleak;
    vlSelfRef.u_core__DOT__d_qleak = vlSelfRef.d_qleak;
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__hlth 
        = vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__hlth;
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__hlth 
        = vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__hlth;
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__hlth 
        = vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__hlth;
    vlSelfRef.u_df__DOT__o_rqen = vlSelfRef.d_rqen;
    vlSelfRef.u_core__DOT__d_rqen = vlSelfRef.d_rqen;
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__i_mode 
        = vlSelfRef.d_mode;
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__i_mode 
        = vlSelfRef.d_mode;
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__i_mode 
        = vlSelfRef.d_mode;
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__i_mode 
        = vlSelfRef.d_mode;
    vlSelfRef.u_df__DOT__o_mode = vlSelfRef.d_mode;
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__i_p0e 
        = vlSelfRef.d_p0e;
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__i_p0e 
        = vlSelfRef.d_p0e;
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__i_p0e 
        = vlSelfRef.d_p0e;
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__i_p0e 
        = vlSelfRef.d_p0e;
    vlSelfRef.u_df__DOT__o_p0e = vlSelfRef.d_p0e;
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__p0 
        = ((IData)(1U) << (IData)(vlSelfRef.d_p0e));
    vlSelfRef.u_df__DOT__o_qdw = vlSelfRef.d_qdw;
    vlSelfRef.u_core__DOT__d_qdw = vlSelfRef.d_qdw;
    vlSelfRef.eg_s_ready = vlSelfRef.u_egbuf__DOT__s_ready;
    vlSelfRef.u_rp__DOT__li_valid = vlSelfRef.li_valid_w;
    vlSelfRef.u_rp__DOT__li_op = vlSelfRef.li_op_w;
    vlSelfRef.u_egbuf__DOT__m_op = vlSelfRef.li_op_w;
    vlSelfRef.u_rp__DOT__li_src = vlSelfRef.li_src_w;
    vlSelfRef.u_egbuf__DOT__m_src = vlSelfRef.li_src_w;
    vlSelfRef.u_rp__DOT__li_dst = vlSelfRef.li_dst_w;
    vlSelfRef.u_egbuf__DOT__m_dst = vlSelfRef.li_dst_w;
    vlSelfRef.u_rp__DOT__li_a0 = vlSelfRef.li_a0_w;
    vlSelfRef.u_egbuf__DOT__m_a0 = vlSelfRef.li_a0_w;
    vlSelfRef.u_rp__DOT__li_a1 = vlSelfRef.li_a1_w;
    vlSelfRef.u_egbuf__DOT__m_a1 = vlSelfRef.li_a1_w;
    vlSelfRef.u_rp__DOT__li_a2 = vlSelfRef.li_a2_w;
    vlSelfRef.u_egbuf__DOT__m_a2 = vlSelfRef.li_a2_w;
    vlSelfRef.u_rp__DOT__li_dat = vlSelfRef.li_dat_w;
    vlSelfRef.u_egbuf__DOT__m_dat = vlSelfRef.li_dat_w;
    vlSelfRef.w_indst = vlSelfRef.u_inbuf__DOT__m_dst;
    vlSelfRef.u_rp__DOT__ld_ready = vlSelfRef.ld_ready;
    vlSelfRef.u_inbuf__DOT__s_ready = vlSelfRef.ld_ready;
    vlSelfRef.u_df__DOT__i_probe = vlSelfRef.w_ftrace;
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__hlend 
        = (vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__hlc 
           >= vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__hlth);
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__rsh 
        = ((IData)(8U) - vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__ridx32);
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__lad 
        = ((IData)(vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__g_lad_sat__DOT__sat)
            ? 0xffffU : (0xffffU & vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__acc));
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__shl2 
        = (0x1fU & ((IData)(vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__wmsb) 
                    + (IData)(vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__wmsb)));
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__hlend 
        = (vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__hlc 
           >= vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__hlth);
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__rsh 
        = ((IData)(8U) - vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__ridx32);
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__lad 
        = ((IData)(vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__g_lad_sat__DOT__sat)
            ? 0xffffU : (0xffffU & vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__acc));
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__shl2 
        = (0x1fU & ((IData)(vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__wmsb) 
                    + (IData)(vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__wmsb)));
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__hlend 
        = (vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__hlc 
           >= vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__hlth);
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__rsh 
        = ((IData)(8U) - vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__ridx32);
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__lad 
        = ((IData)(vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__g_lad_sat__DOT__sat)
            ? 0xffffU : (0xffffU & vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__acc));
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__shl2 
        = (0x1fU & ((IData)(vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__wmsb) 
                    + (IData)(vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__wmsb)));
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__hlend 
        = (vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__hlc 
           >= vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__hlth);
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__rsh 
        = ((IData)(8U) - vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__ridx32);
    vlSelfRef.o_ovf = (0U != (IData)(vlSelfRef.ovf_vec));
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__lad 
        = ((IData)(vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__g_lad_sat__DOT__sat)
            ? 0xffffU : (0xffffU & vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__acc));
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__shl2 
        = (0x1fU & ((IData)(vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__wmsb) 
                    + (IData)(vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__wmsb)));
    vlSelfRef.u_core__DOT__tick_pend = __Vdly__u_core__DOT__tick_pend;
    vlSelfRef.u_core__DOT__refr = __Vdly__u_core__DOT__refr;
    vlSelfRef.u_core__DOT__eidx = __Vdly__u_core__DOT__eidx;
    vlSelfRef.u_core__DOT__wacc = __Vdly__u_core__DOT__wacc;
    vlSelfRef.hb_done = (0U != (IData)(vlSelfRef.done_vec));
    vlSelfRef.d_refr = vlSelfRef.u_df__DOT__dial[6U];
    vlSelfRef.d_thresh = vlSelfRef.u_df__DOT__dial[5U];
    vlSelfRef.df_rstb = vlSelfRef.u_df__DOT__o_rstb;
    vlSelfRef.df_rdata = vlSelfRef.u_df__DOT__o_rdata;
    vlSelfRef.ci_valid = vlSelfRef.u_inbuf__DOT__a_v;
    vlSelfRef.u_core__DOT__eg_live = ((0U == vlSelfRef.u_df__DOT__dial
                                       [0xcU]) | ((IData)(vlSelfRef.u_core__DOT__u_eg__DOT__f) 
                                                  >= 
                                                  vlSelfRef.u_df__DOT__dial
                                                  [0xcU]));
    vlSelfRef.ci_src = (0xfU & (vlSelfRef.u_inbuf__DOT__a_q[2U] 
                                >> 4U));
    vlSelfRef.ci_a0 = (vlSelfRef.u_inbuf__DOT__a_q[1U] 
                       >> 0x10U);
    vlSelfRef.ci_a1 = (0xffffU & vlSelfRef.u_inbuf__DOT__a_q[1U]);
    vlSelfRef.ci_a2 = (vlSelfRef.u_inbuf__DOT__a_q[0U] 
                       >> 0x10U);
    vlSelfRef.ci_dat = (0xffffU & vlSelfRef.u_inbuf__DOT__a_q[0U]);
    vlSelfRef.ci_op = (7U & (vlSelfRef.u_inbuf__DOT__a_q[2U] 
                             >> 8U));
    vlSelfRef.u_core__DOT__state = __Vdly__u_core__DOT__state;
    if (__VdlySet__u_core__DOT__etab__v0) {
        vlSelfRef.u_core__DOT__etab[__VdlyDim0__u_core__DOT__etab__v0] 
            = __VdlyVal__u_core__DOT__etab__v0;
        vlSelfRef.u_core__DOT__ev[__VdlyDim0__u_core__DOT__ev__v0] = 1U;
    }
    if (__VdlySet__u_core__DOT__etab__v1) {
        vlSelfRef.u_core__DOT__etab[0U] = 0U;
        vlSelfRef.u_core__DOT__ev[0U] = 0U;
        vlSelfRef.u_core__DOT__etab[1U] = 0U;
        vlSelfRef.u_core__DOT__ev[1U] = 0U;
        vlSelfRef.u_core__DOT__etab[2U] = 0U;
        vlSelfRef.u_core__DOT__ev[2U] = 0U;
        vlSelfRef.u_core__DOT__etab[3U] = 0U;
        vlSelfRef.u_core__DOT__ev[3U] = 0U;
    }
    vlSelfRef.u_core__DOT__ci_ready = __Vdly__u_core__DOT__ci_ready;
    vlSelfRef.u_core__DOT__lx_valid = __Vdly__u_core__DOT__lx_valid;
    vlSelfRef.u_core__DOT__act = __Vdly__u_core__DOT__act;
    vlSelfRef.u_core__DOT__lo_valid = __Vdly__u_core__DOT__lo_valid;
    vlSelfRef.u_core__DOT__u_eg__DOT__i_kle = vlSelfRef.u_core__DOT__d_kle;
    vlSelfRef.u_core__DOT__u_eg__DOT__fsnap = (((IData)(vlSelfRef.u_core__DOT__u_eg__DOT__fleak) 
                                                <= 
                                                vlSelfRef.u_df__DOT__dial
                                                [0xcU]) 
                                               | ((1U 
                                                   >= (IData)(vlSelfRef.u_core__DOT__u_eg__DOT__fleak)) 
                                                  | ((IData)(vlSelfRef.u_core__DOT__u_eg__DOT__fleak) 
                                                     >= (IData)(vlSelfRef.u_core__DOT__u_eg__DOT__f))));
    vlSelfRef.u_core__DOT__u_eg__DOT__i_floor = vlSelfRef.u_core__DOT__d_floor;
    vlSelfRef.u_core__DOT__eg_gclass = vlSelfRef.u_core__DOT__u_eg__DOT__o_gclass;
    vlSelfRef.u_core__DOT__u_rq__DOT__i_qleak = vlSelfRef.u_core__DOT__d_qleak;
    vlSelfRef.u_core__DOT__u_rq__DOT__i_en = vlSelfRef.u_core__DOT__d_rqen;
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__p0 
        = vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__p0;
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__p0 
        = vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__p0;
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__p0 
        = vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__p0;
    vlSelfRef.u_core__DOT__u_rq__DOT__i_qdw = vlSelfRef.u_core__DOT__d_qdw;
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__addw 
        = (0x1ffffU & VL_SHIFTL_III(17,17,32, vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__c
                                    [(7U & (IData)(vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__ridx))], vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__rsh));
    if (vlSelfRef.d_mode) {
        vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__eng 
            = vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__whs;
        vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__eng 
            = vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__whs;
        vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__eng 
            = vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__whs;
        vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__eng 
            = vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__whs;
    } else {
        vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__eng 
            = vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__lad;
        vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__eng 
            = vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__lad;
        vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__eng 
            = vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__lad;
        vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__eng 
            = vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__lad;
    }
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__ivr 
        = (vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__p0 
           >> (IData)(vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__shl2));
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__addw 
        = (0x1ffffU & VL_SHIFTL_III(17,17,32, vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__c
                                    [(7U & (IData)(vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__ridx))], vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__rsh));
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__ivr 
        = (vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__p0 
           >> (IData)(vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__shl2));
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__addw 
        = (0x1ffffU & VL_SHIFTL_III(17,17,32, vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__c
                                    [(7U & (IData)(vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__ridx))], vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__rsh));
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__ivr 
        = (vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__p0 
           >> (IData)(vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__shl2));
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__addw 
        = (0x1ffffU & VL_SHIFTL_III(17,17,32, vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__c
                                    [(7U & (IData)(vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__ridx))], vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__rsh));
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__ivr 
        = (vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__p0 
           >> (IData)(vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__shl2));
    vlSelfRef.u_core__DOT__hb_done = vlSelfRef.hb_done;
    vlSelfRef.u_core__DOT__d_refr = vlSelfRef.d_refr;
    vlSelfRef.u_core__DOT__d_thresh = vlSelfRef.d_thresh;
    vlSelfRef.u_core__DOT__df_rstb = vlSelfRef.df_rstb;
    vlSelfRef.u_core__DOT__df_rdata = vlSelfRef.df_rdata;
    vlSelfRef.u_core__DOT__ci_valid = vlSelfRef.ci_valid;
    vlSelfRef.u_core__DOT__u_eg__DOT__i_fire = vlSelfRef.u_core__DOT__eg_fire;
    vlSelfRef.u_core__DOT__eff_pe = (((QData)((IData)(
                                                      (7U 
                                                       & (- (IData)(
                                                                    (1U 
                                                                     & (IData)(
                                                                               (vlSelfRef.u_core__DOT__eff_p 
                                                                                >> 0x20U)))))))) 
                                      << 0x21U) | vlSelfRef.u_core__DOT__eff_p);
    vlSelfRef.u_core__DOT__u_eg__DOT__o_live = vlSelfRef.u_core__DOT__eg_live;
    vlSelfRef.w_cid = vlSelfRef.u_core__DOT__cell_id;
    vlSelfRef.w_bound = vlSelfRef.u_core__DOT__bound;
    vlSelfRef.u_core__DOT__ci_src = vlSelfRef.ci_src;
    vlSelfRef.u_inbuf__DOT__m_src = vlSelfRef.ci_src;
    vlSelfRef.u_core__DOT__ci_a0 = vlSelfRef.ci_a0;
    vlSelfRef.u_inbuf__DOT__m_a0 = vlSelfRef.ci_a0;
    vlSelfRef.u_core__DOT__ci_a1 = vlSelfRef.ci_a1;
    vlSelfRef.u_inbuf__DOT__m_a1 = vlSelfRef.ci_a1;
    vlSelfRef.u_core__DOT__ci_a2 = vlSelfRef.ci_a2;
    vlSelfRef.u_inbuf__DOT__m_a2 = vlSelfRef.ci_a2;
    vlSelfRef.u_core__DOT__ci_dat = vlSelfRef.ci_dat;
    vlSelfRef.u_inbuf__DOT__m_dat = vlSelfRef.ci_dat;
    vlSelfRef.u_core__DOT__ci_op = vlSelfRef.ci_op;
    vlSelfRef.u_inbuf__DOT__m_op = vlSelfRef.ci_op;
    vlSelfRef.df_rd = vlSelfRef.u_core__DOT__df_rd;
    vlSelfRef.u_core__DOT__eg_tick = (0x11U == (IData)(vlSelfRef.u_core__DOT__state));
    vlSelfRef.df_wr = vlSelfRef.u_core__DOT__df_wr;
    vlSelfRef.df_wr_g = ((IData)(vlSelfRef.i_bdf_wr) 
                         | (IData)(vlSelfRef.u_core__DOT__df_wr));
    vlSelfRef.u_inbuf__DOT__pop = ((IData)(vlSelfRef.u_core__DOT__ci_ready) 
                                   & (IData)(vlSelfRef.u_inbuf__DOT__a_v));
    vlSelfRef.ci_ready_w = vlSelfRef.u_core__DOT__ci_ready;
    vlSelfRef.df_addr = vlSelfRef.u_core__DOT__df_addr;
    if (vlSelfRef.i_bdf_wr) {
        vlSelfRef.df_addr_g = vlSelfRef.i_bdf_addr;
        vlSelfRef.df_wdata_g = vlSelfRef.i_bdf_wdata;
    } else {
        vlSelfRef.df_addr_g = vlSelfRef.u_core__DOT__df_addr;
        vlSelfRef.df_wdata_g = vlSelfRef.u_core__DOT__df_wdata;
    }
    vlSelfRef.df_wdata = vlSelfRef.u_core__DOT__df_wdata;
    vlSelfRef.lx_valid = vlSelfRef.u_core__DOT__lx_valid;
    vlSelfRef.w_act = vlSelfRef.u_core__DOT__act;
    vlSelfRef.u_core__DOT__act_e = (((QData)((IData)(
                                                     (0xfffffU 
                                                      & (- (IData)(
                                                                   (1U 
                                                                    & ((IData)(vlSelfRef.u_core__DOT__act) 
                                                                       >> 0xfU))))))) 
                                     << 0x10U) | (QData)((IData)(vlSelfRef.u_core__DOT__act)));
    vlSelfRef.hb_base = vlSelfRef.u_core__DOT__hb_base;
    vlSelfRef.u_core__DOT__prod_p = (0x1ffffffffULL 
                                     & VL_MULS_QQQ(33, 
                                                   (0x1ffffffffULL 
                                                    & VL_EXTENDS_QI(33,17, (IData)(vlSelfRef.u_core__DOT__eff_w))), 
                                                   (0x1ffffffffULL 
                                                    & VL_EXTENDS_QI(33,16, (IData)(vlSelfRef.u_core__DOT__lr_dat)))));
    vlSelfRef.lx_op = vlSelfRef.u_core__DOT__lx_op;
    vlSelfRef.lx_dst = vlSelfRef.u_core__DOT__lx_dst;
    vlSelfRef.lx_src = vlSelfRef.u_core__DOT__lx_src;
    vlSelfRef.lx_dat = vlSelfRef.u_core__DOT__lx_dat;
    vlSelfRef.lx_a0 = vlSelfRef.u_core__DOT__lx_a0;
    vlSelfRef.lx_a1 = vlSelfRef.u_core__DOT__lx_a1;
    vlSelfRef.lx_a2 = vlSelfRef.u_core__DOT__lx_a2;
    vlSelfRef.lo_op = vlSelfRef.u_core__DOT__lo_op;
    vlSelfRef.lo_dst = vlSelfRef.u_core__DOT__lo_dst;
    vlSelfRef.lo_src = vlSelfRef.u_core__DOT__lo_src;
    vlSelfRef.lo_a0 = vlSelfRef.u_core__DOT__lo_a0;
    vlSelfRef.lo_a1 = vlSelfRef.u_core__DOT__lo_a1;
    vlSelfRef.lo_a2 = vlSelfRef.u_core__DOT__lo_a2;
    vlSelfRef.lo_dat = vlSelfRef.u_core__DOT__lo_dat;
    vlSelfRef.u_core__DOT__rq_tick = (2U == (IData)(vlSelfRef.u_core__DOT__hb_cmd));
    vlSelfRef.hb_cmd = vlSelfRef.u_core__DOT__hb_cmd;
    vlSelfRef.u_core__DOT__rq_train = (5U == (IData)(vlSelfRef.u_core__DOT__hb_cmd));
    vlSelfRef.u_core__DOT__u_rq__DOT__i_gclass = vlSelfRef.u_core__DOT__hb_gcl;
    vlSelfRef.hb_gcl = vlSelfRef.u_core__DOT__hb_gcl;
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__gcl 
        = ((8U <= (IData)(vlSelfRef.u_core__DOT__hb_gcl))
            ? 7U : (IData)(vlSelfRef.u_core__DOT__hb_gcl));
    vlSelfRef.lo_valid = vlSelfRef.u_core__DOT__lo_valid;
    vlSelfRef.lo_grant = (1U & ((~ (IData)(vlSelfRef.u_core__DOT__lo_valid)) 
                                | (IData)(vlSelfRef.u_egbuf__DOT__s_ready)));
    vlSelfRef.lx_grant = ((~ (IData)(vlSelfRef.u_core__DOT__lo_valid)) 
                          & (IData)(vlSelfRef.u_egbuf__DOT__s_ready));
    vlSelfRef.eg_s_valid = ((IData)(vlSelfRef.u_core__DOT__lo_valid) 
                            | (IData)(vlSelfRef.u_core__DOT__lx_valid));
    if (vlSelfRef.u_core__DOT__lo_valid) {
        vlSelfRef.eg_op = vlSelfRef.u_core__DOT__lo_op;
        vlSelfRef.eg_src = vlSelfRef.u_core__DOT__lo_src;
        vlSelfRef.eg_dst = vlSelfRef.u_core__DOT__lo_dst;
        vlSelfRef.eg_a0 = vlSelfRef.u_core__DOT__lo_a0;
        vlSelfRef.eg_a1 = vlSelfRef.u_core__DOT__lo_a1;
        vlSelfRef.eg_a2 = vlSelfRef.u_core__DOT__lo_a2;
        vlSelfRef.eg_dat = vlSelfRef.u_core__DOT__lo_dat;
    } else {
        vlSelfRef.eg_op = vlSelfRef.u_core__DOT__lx_op;
        vlSelfRef.eg_src = vlSelfRef.u_core__DOT__lx_src;
        vlSelfRef.eg_dst = vlSelfRef.u_core__DOT__lx_dst;
        vlSelfRef.eg_a0 = vlSelfRef.u_core__DOT__lx_a0;
        vlSelfRef.eg_a1 = vlSelfRef.u_core__DOT__lx_a1;
        vlSelfRef.eg_a2 = vlSelfRef.u_core__DOT__lx_a2;
        vlSelfRef.eg_dat = vlSelfRef.u_core__DOT__lx_dat;
    }
    vlSelfRef.u_core__DOT__u_rq__DOT__i_sel = vlSelfRef.u_core__DOT__hb_sel;
    vlSelfRef.u_core__DOT__u_rq__DOT__esel = 0U;
    if ((1U & (IData)(vlSelfRef.u_core__DOT__hb_sel))) {
        vlSelfRef.u_core__DOT__u_rq__DOT__esel = 0U;
    }
    if ((2U & (IData)(vlSelfRef.u_core__DOT__hb_sel))) {
        vlSelfRef.u_core__DOT__u_rq__DOT__esel = 1U;
    }
    if ((4U & (IData)(vlSelfRef.u_core__DOT__hb_sel))) {
        vlSelfRef.u_core__DOT__u_rq__DOT__esel = 2U;
    }
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__i_sel 
        = (1U & ((IData)(vlSelfRef.u_core__DOT__hb_sel) 
                 >> 0U));
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__i_sel 
        = (1U & ((IData)(vlSelfRef.u_core__DOT__hb_sel) 
                 >> 1U));
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__i_sel 
        = (1U & ((IData)(vlSelfRef.u_core__DOT__hb_sel) 
                 >> 2U));
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__i_sel 
        = (1U & ((IData)(vlSelfRef.u_core__DOT__hb_sel) 
                 >> 3U));
    vlSelfRef.hb_sel = vlSelfRef.u_core__DOT__hb_sel;
    vlSelfRef.u_core__DOT__u_rq__DOT__rsel = 0U;
    if ((1U & (IData)(vlSelfRef.u_core__DOT__hb_sel))) {
        vlSelfRef.u_core__DOT__u_rq__DOT__rsel = vlSelfRef.u_core__DOT__u_rq__DOT__R
            [0U];
    }
    if ((2U & (IData)(vlSelfRef.u_core__DOT__hb_sel))) {
        vlSelfRef.u_core__DOT__u_rq__DOT__rsel = vlSelfRef.u_core__DOT__u_rq__DOT__R
            [1U];
    }
    if ((4U & (IData)(vlSelfRef.u_core__DOT__hb_sel))) {
        vlSelfRef.u_core__DOT__u_rq__DOT__rsel = vlSelfRef.u_core__DOT__u_rq__DOT__R
            [2U];
    }
    if ((8U & (IData)(vlSelfRef.u_core__DOT__hb_sel))) {
        vlSelfRef.u_core__DOT__u_rq__DOT__esel = 3U;
        vlSelfRef.u_core__DOT__u_rq__DOT__rsel = vlSelfRef.u_core__DOT__u_rq__DOT__R
            [3U];
    }
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__wfin 
        = (0x1ffffU & ((IData)(vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__base) 
                       + (IData)(vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__eng)));
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__ival 
        = ((0U == vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__ivr)
            ? 1U : vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__ivr);
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__wfin 
        = (0x1ffffU & ((IData)(vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__base) 
                       + (IData)(vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__eng)));
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__ival 
        = ((0U == vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__ivr)
            ? 1U : vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__ivr);
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__wfin 
        = (0x1ffffU & ((IData)(vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__base) 
                       + (IData)(vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__eng)));
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__ival 
        = ((0U == vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__ivr)
            ? 1U : vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__ivr);
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__wfin 
        = (0x1ffffU & ((IData)(vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__base) 
                       + (IData)(vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__eng)));
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__ival 
        = ((0U == vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__ivr)
            ? 1U : vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__ivr);
    vlSelfRef.u_df__DOT__i_rd = vlSelfRef.df_rd;
    vlSelfRef.u_core__DOT__u_eg__DOT__i_tick = vlSelfRef.u_core__DOT__eg_tick;
    vlSelfRef.u_df__DOT__i_wr = vlSelfRef.df_wr_g;
    vlSelfRef.u_inbuf__DOT__m_ready = vlSelfRef.ci_ready_w;
    vlSelfRef.u_df__DOT__i_addr = vlSelfRef.df_addr_g;
    vlSelfRef.u_df__DOT__i_wdata = vlSelfRef.df_wdata_g;
    vlSelfRef.u_core__DOT__leak_sum = (0xfffffffffULL 
                                       & (vlSelfRef.u_core__DOT__act_e 
                                          - VL_SHIFTRS_QQI(36,36,4, vlSelfRef.u_core__DOT__act_e, (IData)(vlSelfRef.d_ka))));
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__i_base 
        = vlSelfRef.hb_base;
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__i_base 
        = vlSelfRef.hb_base;
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__i_base 
        = vlSelfRef.hb_base;
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__i_base 
        = vlSelfRef.hb_base;
    vlSelfRef.u_core__DOT__u_rq__DOT__i_tick = vlSelfRef.u_core__DOT__rq_tick;
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__i_cmd 
        = vlSelfRef.hb_cmd;
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__i_cmd 
        = vlSelfRef.hb_cmd;
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__i_cmd 
        = vlSelfRef.hb_cmd;
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__i_cmd 
        = vlSelfRef.hb_cmd;
    vlSelfRef.u_core__DOT__u_rq__DOT__i_train = vlSelfRef.u_core__DOT__rq_train;
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__i_gclass 
        = vlSelfRef.hb_gcl;
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__i_gclass 
        = vlSelfRef.hb_gcl;
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__i_gclass 
        = vlSelfRef.hb_gcl;
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__i_gclass 
        = vlSelfRef.hb_gcl;
    vlSelfRef.u_core__DOT__u_rq__DOT__gcl = vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__gcl;
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__gcl 
        = vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__gcl;
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__gcl 
        = vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__gcl;
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__gcl 
        = vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__gcl;
    vlSelfRef.u_core__DOT__u_rq__DOT__dsh = (0x3fU 
                                             & (((IData)(8U) 
                                                 + (IData)(vlSelfRef.d_qdw)) 
                                                - (IData)(vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__gcl)));
    vlSelfRef.u_core__DOT__lo_ready = vlSelfRef.lo_grant;
    vlSelfRef.u_core__DOT__lx_ready = vlSelfRef.lx_grant;
    vlSelfRef.u_egbuf__DOT__s_valid = vlSelfRef.eg_s_valid;
    vlSelfRef.u_egbuf__DOT__push = ((IData)(vlSelfRef.u_egbuf__DOT__s_ready) 
                                    & (IData)(vlSelfRef.eg_s_valid));
    vlSelfRef.u_egbuf__DOT__s_op = vlSelfRef.eg_op;
    vlSelfRef.u_egbuf__DOT__s_src = vlSelfRef.eg_src;
    vlSelfRef.u_egbuf__DOT__s_dst = vlSelfRef.eg_dst;
    vlSelfRef.u_egbuf__DOT__s_a0 = vlSelfRef.eg_a0;
    vlSelfRef.u_egbuf__DOT__s_a1 = vlSelfRef.eg_a1;
    vlSelfRef.u_egbuf__DOT__s_a2 = vlSelfRef.eg_a2;
    vlSelfRef.u_egbuf__DOT__s_dat = vlSelfRef.eg_dat;
    vlSelfRef.u_egbuf__DOT__s_bus[0U] = (IData)((((QData)((IData)(vlSelfRef.eg_a0)) 
                                                  << 0x30U) 
                                                 | (((QData)((IData)(
                                                                     (((IData)(vlSelfRef.eg_a1) 
                                                                       << 0x10U) 
                                                                      | (IData)(vlSelfRef.eg_a2)))) 
                                                     << 0x10U) 
                                                    | (QData)((IData)(vlSelfRef.eg_dat)))));
    vlSelfRef.u_egbuf__DOT__s_bus[1U] = (IData)(((((QData)((IData)(vlSelfRef.eg_a0)) 
                                                   << 0x30U) 
                                                  | (((QData)((IData)(
                                                                      (((IData)(vlSelfRef.eg_a1) 
                                                                        << 0x10U) 
                                                                       | (IData)(vlSelfRef.eg_a2)))) 
                                                      << 0x10U) 
                                                     | (QData)((IData)(vlSelfRef.eg_dat)))) 
                                                 >> 0x20U));
    vlSelfRef.u_egbuf__DOT__s_bus[2U] = (((IData)(vlSelfRef.eg_op) 
                                          << 8U) | 
                                         (((IData)(vlSelfRef.eg_src) 
                                           << 4U) | (IData)(vlSelfRef.eg_dst)));
    vlSelfRef.hb_w_mux = 0U;
    if ((1U & (IData)(vlSelfRef.hb_sel))) {
        vlSelfRef.hb_w_mux = (0xffffU & (IData)(vlSelfRef.w_flat));
    }
    if ((2U & (IData)(vlSelfRef.hb_sel))) {
        vlSelfRef.hb_w_mux = (0xffffU & (IData)((vlSelfRef.w_flat 
                                                 >> 0x10U)));
    }
    if ((4U & (IData)(vlSelfRef.hb_sel))) {
        vlSelfRef.hb_w_mux = (0xffffU & (IData)((vlSelfRef.w_flat 
                                                 >> 0x20U)));
    }
    if ((8U & (IData)(vlSelfRef.hb_sel))) {
        vlSelfRef.hb_w_mux = (0xffffU & (IData)((vlSelfRef.w_flat 
                                                 >> 0x30U)));
    }
    vlSelfRef.u_core__DOT__u_rq__DOT__rleak = (0xffffU 
                                               & ((IData)(vlSelfRef.u_core__DOT__u_rq__DOT__rsel) 
                                                  - 
                                                  ((IData)(vlSelfRef.u_core__DOT__u_rq__DOT__rsel) 
                                                   >> (IData)(vlSelfRef.d_qleak))));
    vlSelfRef.u_core__DOT__u_rq__DOT__cred_cur = ((IData)(vlSelfRef.u_core__DOT__u_rq__DOT__rsel) 
                                                  >> (IData)(vlSelfRef.d_qdw));
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__wout 
        = ((0x10000U & vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__wfin)
            ? 0xffffU : (0xffffU & vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__wfin));
    vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__decn 
        = ((0U != (IData)(vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__wh)) 
           & (vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__agen 
              >= vlSelfRef.edges__BRA__1__KET____DOT__u_hebb__DOT__ival));
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__wout 
        = ((0x10000U & vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__wfin)
            ? 0xffffU : (0xffffU & vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__wfin));
    vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__decn 
        = ((0U != (IData)(vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__wh)) 
           & (vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__agen 
              >= vlSelfRef.edges__BRA__2__KET____DOT__u_hebb__DOT__ival));
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__wout 
        = ((0x10000U & vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__wfin)
            ? 0xffffU : (0xffffU & vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__wfin));
    vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__decn 
        = ((0U != (IData)(vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__wh)) 
           & (vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__agen 
              >= vlSelfRef.edges__BRA__3__KET____DOT__u_hebb__DOT__ival));
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__wout 
        = ((0x10000U & vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__wfin)
            ? 0xffffU : (0xffffU & vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__wfin));
    vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__decn 
        = ((0U != (IData)(vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__wh)) 
           & (vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__agen 
              >= vlSelfRef.edges__BRA__0__KET____DOT__u_hebb__DOT__ival));
    vlSelfRef.u_core__DOT__u_rq__DOT__qbase = VL_SHIFTL_III(32,32,6, (IData)(1U), (IData)(vlSelfRef.u_core__DOT__u_rq__DOT__dsh));
    vlSelfRef.hb_w = vlSelfRef.hb_w_mux;
    vlSelfRef.u_core__DOT__u_rq__DOT__rsnap = ((1U 
                                                >= (IData)(vlSelfRef.u_core__DOT__u_rq__DOT__rleak)) 
                                               | ((IData)(vlSelfRef.u_core__DOT__u_rq__DOT__rleak) 
                                                  >= (IData)(vlSelfRef.u_core__DOT__u_rq__DOT__rsel)));
    vlSelfRef.u_core__DOT__rq_credit = ((IData)(vlSelfRef.d_rqen)
                                         ? (0xffffU 
                                            & vlSelfRef.u_core__DOT__u_rq__DOT__cred_cur)
                                         : 0U);
    vlSelfRef.u_core__DOT__u_rq__DOT__dep = (VL_SHIFTR_III(32,32,32, vlSelfRef.u_core__DOT__u_rq__DOT__qbase, 2U) 
                                             + VL_SHIFTR_III(32,32,32, vlSelfRef.u_core__DOT__u_rq__DOT__qbase, 5U));
    vlSelfRef.u_core__DOT__hb_w = vlSelfRef.hb_w;
    vlSelfRef.u_core__DOT__u_rq__DOT__rleakn = ((IData)(vlSelfRef.u_core__DOT__u_rq__DOT__rsnap)
                                                 ? 0U
                                                 : (IData)(vlSelfRef.u_core__DOT__u_rq__DOT__rleak));
    vlSelfRef.u_core__DOT__u_rq__DOT__o_credit = vlSelfRef.u_core__DOT__rq_credit;
    vlSelfRef.u_core__DOT__w_rq = (0x1ffffU & ((IData)(vlSelfRef.hb_w_mux) 
                                               + (IData)(vlSelfRef.u_core__DOT__rq_credit)));
    vlSelfRef.u_core__DOT__u_rq__DOT__rsum = (0x1ffffffffULL 
                                              & ((QData)((IData)(vlSelfRef.u_core__DOT__u_rq__DOT__rsel)) 
                                                 + (QData)((IData)(vlSelfRef.u_core__DOT__u_rq__DOT__dep))));
    vlSelfRef.u_core__DOT__hb_wq = ((0x10000U & vlSelfRef.u_core__DOT__w_rq)
                                     ? 0xffffU : (0xffffU 
                                                  & vlSelfRef.u_core__DOT__w_rq));
    vlSelfRef.u_core__DOT__u_rq__DOT__rsat = (vlSelfRef.u_core__DOT__u_rq__DOT__rsum 
                                              > vlSelfRef.u_core__DOT__u_rq__DOT__rfull);
    vlSelfRef.u_core__DOT__prod = (0x1ffffffffULL & 
                                   VL_MULS_QQQ(33, 
                                               (0x1ffffffffULL 
                                                & VL_EXTENDS_QI(33,17, (IData)(vlSelfRef.u_core__DOT__hb_wq))), 
                                               (0x1ffffffffULL 
                                                & VL_EXTENDS_QI(33,16, (IData)(vlSelfRef.u_core__DOT__lr_dat)))));
    vlSelfRef.u_core__DOT__u_rq__DOT__rdepn = ((IData)(vlSelfRef.u_core__DOT__u_rq__DOT__rsat)
                                                ? 0xffffU
                                                : (0xffffU 
                                                   & (IData)(vlSelfRef.u_core__DOT__u_rq__DOT__rsum)));
    vlSelfRef.u_core__DOT__prod_e = (((QData)((IData)(
                                                      (7U 
                                                       & (- (IData)(
                                                                    (1U 
                                                                     & (IData)(
                                                                               (vlSelfRef.u_core__DOT__prod 
                                                                                >> 0x20U)))))))) 
                                      << 0x21U) | vlSelfRef.u_core__DOT__prod);
    vlSelfRef.u_core__DOT__u_rq__DOT__cred_new = ((IData)(vlSelfRef.u_core__DOT__u_rq__DOT__rdepn) 
                                                  >> (IData)(vlSelfRef.d_qdw));
    vlSelfRef.u_core__DOT__eff_sum = (0xfffffffffULL 
                                      & (vlSelfRef.u_core__DOT__act_e 
                                         + VL_SHIFTRS_QQI(36,36,32, vlSelfRef.u_core__DOT__prod_e, 0xfU)));
    vlSelfRef.u_core__DOT__u_rq__DOT__o_antic = ((IData)(vlSelfRef.d_rqen) 
                                                 & ((IData)(vlSelfRef.u_core__DOT__rq_train) 
                                                    & (vlSelfRef.u_core__DOT__u_rq__DOT__cred_new 
                                                       > vlSelfRef.u_core__DOT__u_rq__DOT__cred_cur)));
    vlSelfRef.u_core__DOT__o_antic = vlSelfRef.u_core__DOT__u_rq__DOT__o_antic;
    vlSelfRef.w_antic = vlSelfRef.u_core__DOT__u_rq__DOT__o_antic;
}
