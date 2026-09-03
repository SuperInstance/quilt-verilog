// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Model implementation (design independent parts)

#include "Vq_wall_gate__pch.h"

//============================================================
// Constructors

Vq_wall_gate::Vq_wall_gate(VerilatedContext* _vcontextp__, const char* _vcname__)
    : VerilatedModel{*_vcontextp__}
    , vlSymsp{new Vq_wall_gate__Syms(contextp(), _vcname__, this)}
    , clk{vlSymsp->TOP.clk}
    , rst_n{vlSymsp->TOP.rst_n}
    , i_go{vlSymsp->TOP.i_go}
    , o_running{vlSymsp->TOP.o_running}
    , o_bail{vlSymsp->TOP.o_bail}
    , o_tval{vlSymsp->TOP.o_tval}
    , o_cflag{vlSymsp->TOP.o_cflag}
    , o_nf{vlSymsp->TOP.o_nf}
    , o_gopen{vlSymsp->TOP.o_gopen}
    , o_em_mask{vlSymsp->TOP.o_em_mask}
    , o_t{vlSymsp->TOP.o_t}
    , i_seed{vlSymsp->TOP.i_seed}
    , o_em_pm{vlSymsp->TOP.o_em_pm}
    , o_em_e{vlSymsp->TOP.o_em_e}
    , i_lats{vlSymsp->TOP.i_lats}
    , o_resid{vlSymsp->TOP.o_resid}
    , o_events{vlSymsp->TOP.o_events}
    , o_mass{vlSymsp->TOP.o_mass}
    , o_cancels{vlSymsp->TOP.o_cancels}
    , o_chatter{vlSymsp->TOP.o_chatter}
    , o_settles{vlSymsp->TOP.o_settles}
    , o_gopen_tot{vlSymsp->TOP.o_gopen_tot}
    , o_gcomp{vlSymsp->TOP.o_gcomp}
    , rootp{&(vlSymsp->TOP)}
{
    // Register model with the context
    contextp()->addModel(this);
}

Vq_wall_gate::Vq_wall_gate(const char* _vcname__)
    : Vq_wall_gate(Verilated::threadContextp(), _vcname__)
{
}

//============================================================
// Destructor

Vq_wall_gate::~Vq_wall_gate() {
    delete vlSymsp;
}

//============================================================
// Evaluation function

#ifdef VL_DEBUG
void Vq_wall_gate___024root___eval_debug_assertions(Vq_wall_gate___024root* vlSelf);
#endif  // VL_DEBUG
void Vq_wall_gate___024root___eval_static(Vq_wall_gate___024root* vlSelf);
void Vq_wall_gate___024root___eval_initial(Vq_wall_gate___024root* vlSelf);
void Vq_wall_gate___024root___eval_settle(Vq_wall_gate___024root* vlSelf);
void Vq_wall_gate___024root___eval(Vq_wall_gate___024root* vlSelf);

void Vq_wall_gate::eval_step() {
    VL_DEBUG_IF(VL_DBG_MSGF("+++++TOP Evaluate Vq_wall_gate::eval_step\n"); );
#ifdef VL_DEBUG
    // Debug assertions
    Vq_wall_gate___024root___eval_debug_assertions(&(vlSymsp->TOP));
#endif  // VL_DEBUG
    vlSymsp->__Vm_deleter.deleteAll();
    if (VL_UNLIKELY(!vlSymsp->__Vm_didInit)) {
        vlSymsp->__Vm_didInit = true;
        VL_DEBUG_IF(VL_DBG_MSGF("+ Initial\n"););
        Vq_wall_gate___024root___eval_static(&(vlSymsp->TOP));
        Vq_wall_gate___024root___eval_initial(&(vlSymsp->TOP));
        Vq_wall_gate___024root___eval_settle(&(vlSymsp->TOP));
    }
    VL_DEBUG_IF(VL_DBG_MSGF("+ Eval\n"););
    Vq_wall_gate___024root___eval(&(vlSymsp->TOP));
    // Evaluate cleanup
    Verilated::endOfEval(vlSymsp->__Vm_evalMsgQp);
}

//============================================================
// Events and timing
bool Vq_wall_gate::eventsPending() { return false; }

uint64_t Vq_wall_gate::nextTimeSlot() {
    VL_FATAL_MT(__FILE__, __LINE__, "", "No delays in the design");
    return 0;
}

//============================================================
// Utilities

const char* Vq_wall_gate::name() const {
    return vlSymsp->name();
}

//============================================================
// Invoke final blocks

void Vq_wall_gate___024root___eval_final(Vq_wall_gate___024root* vlSelf);

VL_ATTR_COLD void Vq_wall_gate::final() {
    Vq_wall_gate___024root___eval_final(&(vlSymsp->TOP));
}

//============================================================
// Implementations of abstract methods from VerilatedModel

const char* Vq_wall_gate::hierName() const { return vlSymsp->name(); }
const char* Vq_wall_gate::modelName() const { return "Vq_wall_gate"; }
unsigned Vq_wall_gate::threads() const { return 1; }
void Vq_wall_gate::prepareClone() const { contextp()->prepareClone(); }
void Vq_wall_gate::atClone() const {
    contextp()->threadPoolpOnClone();
}
