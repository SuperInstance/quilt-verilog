// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Symbol table internal header
//
// Internal details; most calling programs do not need this header,
// unless using verilator public meta comments.

#ifndef VERILATED_VQ_WALL_GATE__SYMS_H_
#define VERILATED_VQ_WALL_GATE__SYMS_H_  // guard

#include "verilated.h"

// INCLUDE MODEL CLASS

#include "Vq_wall_gate.h"

// INCLUDE MODULE CLASSES
#include "Vq_wall_gate___024root.h"

// SYMS CLASS (contains all model state)
class alignas(VL_CACHE_LINE_BYTES)Vq_wall_gate__Syms final : public VerilatedSyms {
  public:
    // INTERNAL STATE
    Vq_wall_gate* const __Vm_modelp;
    VlDeleter __Vm_deleter;
    bool __Vm_didInit = false;

    // MODULE INSTANCE STATE
    Vq_wall_gate___024root         TOP;

    // CONSTRUCTORS
    Vq_wall_gate__Syms(VerilatedContext* contextp, const char* namep, Vq_wall_gate* modelp);
    ~Vq_wall_gate__Syms();

    // METHODS
    const char* name() { return TOP.name(); }
};

#endif  // guard
