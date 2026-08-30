// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Model implementation (design independent parts)

#include "Vq_fabric_top__pch.h"

//============================================================
// Constructors

Vq_fabric_top::Vq_fabric_top(VerilatedContext* _vcontextp__, const char* _vcname__)
    : VerilatedModel{*_vcontextp__}
    , vlSymsp{new Vq_fabric_top__Syms(contextp(), _vcname__, this)}
    , clk{vlSymsp->TOP.clk}
    , rst_n{vlSymsp->TOP.rst_n}
    , i_val{vlSymsp->TOP.i_val}
    , o_rdy{vlSymsp->TOP.o_rdy}
    , i_op{vlSymsp->TOP.i_op}
    , i_src{vlSymsp->TOP.i_src}
    , i_dst{vlSymsp->TOP.i_dst}
    , o_val{vlSymsp->TOP.o_val}
    , i_rdy{vlSymsp->TOP.i_rdy}
    , o_op{vlSymsp->TOP.o_op}
    , o_src{vlSymsp->TOP.o_src}
    , o_dst{vlSymsp->TOP.o_dst}
    , o_ovf{vlSymsp->TOP.o_ovf}
    , i_a0{vlSymsp->TOP.i_a0}
    , i_a1{vlSymsp->TOP.i_a1}
    , i_a2{vlSymsp->TOP.i_a2}
    , i_dat{vlSymsp->TOP.i_dat}
    , o_a0{vlSymsp->TOP.o_a0}
    , o_a1{vlSymsp->TOP.o_a1}
    , o_a2{vlSymsp->TOP.o_a2}
    , o_dat{vlSymsp->TOP.o_dat}
    , __PVT__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell{vlSymsp->TOP.__PVT__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell}
    , __PVT__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell{vlSymsp->TOP.__PVT__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell}
    , __PVT__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__connc__DOT__u_cell{vlSymsp->TOP.__PVT__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__connc__DOT__u_cell}
    , __PVT__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell{vlSymsp->TOP.__PVT__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell}
    , __PVT__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__connc__DOT__u_cell{vlSymsp->TOP.__PVT__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__connc__DOT__u_cell}
    , __PVT__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell{vlSymsp->TOP.__PVT__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell}
    , __PVT__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__connc__DOT__u_cell{vlSymsp->TOP.__PVT__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__connc__DOT__u_cell}
    , __PVT__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell{vlSymsp->TOP.__PVT__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell}
    , __PVT__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__connc__DOT__u_cell{vlSymsp->TOP.__PVT__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__connc__DOT__u_cell}
    , __PVT__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell{vlSymsp->TOP.__PVT__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell}
    , __PVT__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__connc__DOT__u_cell{vlSymsp->TOP.__PVT__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__connc__DOT__u_cell}
    , __PVT__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell{vlSymsp->TOP.__PVT__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell}
    , __PVT__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell{vlSymsp->TOP.__PVT__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell}
    , __PVT__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell{vlSymsp->TOP.__PVT__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell}
    , __PVT__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell{vlSymsp->TOP.__PVT__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell}
    , rootp{&(vlSymsp->TOP)}
{
    // Register model with the context
    contextp()->addModel(this);
}

Vq_fabric_top::Vq_fabric_top(const char* _vcname__)
    : Vq_fabric_top(Verilated::threadContextp(), _vcname__)
{
}

//============================================================
// Destructor

Vq_fabric_top::~Vq_fabric_top() {
    delete vlSymsp;
}

//============================================================
// Evaluation function

#ifdef VL_DEBUG
void Vq_fabric_top___024root___eval_debug_assertions(Vq_fabric_top___024root* vlSelf);
#endif  // VL_DEBUG
void Vq_fabric_top___024root___eval_static(Vq_fabric_top___024root* vlSelf);
void Vq_fabric_top___024root___eval_initial(Vq_fabric_top___024root* vlSelf);
void Vq_fabric_top___024root___eval_settle(Vq_fabric_top___024root* vlSelf);
void Vq_fabric_top___024root___eval(Vq_fabric_top___024root* vlSelf);

void Vq_fabric_top::eval_step() {
    VL_DEBUG_IF(VL_DBG_MSGF("+++++TOP Evaluate Vq_fabric_top::eval_step\n"); );
#ifdef VL_DEBUG
    // Debug assertions
    Vq_fabric_top___024root___eval_debug_assertions(&(vlSymsp->TOP));
#endif  // VL_DEBUG
    vlSymsp->__Vm_deleter.deleteAll();
    if (VL_UNLIKELY(!vlSymsp->__Vm_didInit)) {
        vlSymsp->__Vm_didInit = true;
        VL_DEBUG_IF(VL_DBG_MSGF("+ Initial\n"););
        Vq_fabric_top___024root___eval_static(&(vlSymsp->TOP));
        Vq_fabric_top___024root___eval_initial(&(vlSymsp->TOP));
        Vq_fabric_top___024root___eval_settle(&(vlSymsp->TOP));
    }
    VL_DEBUG_IF(VL_DBG_MSGF("+ Eval\n"););
    Vq_fabric_top___024root___eval(&(vlSymsp->TOP));
    // Evaluate cleanup
    Verilated::endOfEval(vlSymsp->__Vm_evalMsgQp);
}

//============================================================
// Events and timing
bool Vq_fabric_top::eventsPending() { return false; }

uint64_t Vq_fabric_top::nextTimeSlot() {
    VL_FATAL_MT(__FILE__, __LINE__, "", "%Error: No delays in the design");
    return 0;
}

//============================================================
// Utilities

const char* Vq_fabric_top::name() const {
    return vlSymsp->name();
}

//============================================================
// Invoke final blocks

void Vq_fabric_top___024root___eval_final(Vq_fabric_top___024root* vlSelf);

VL_ATTR_COLD void Vq_fabric_top::final() {
    Vq_fabric_top___024root___eval_final(&(vlSymsp->TOP));
}

//============================================================
// Implementations of abstract methods from VerilatedModel

const char* Vq_fabric_top::hierName() const { return vlSymsp->name(); }
const char* Vq_fabric_top::modelName() const { return "Vq_fabric_top"; }
unsigned Vq_fabric_top::threads() const { return 1; }
void Vq_fabric_top::prepareClone() const { contextp()->prepareClone(); }
void Vq_fabric_top::atClone() const {
    contextp()->threadPoolpOnClone();
}
