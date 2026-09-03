// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Primary model header
//
// This header should be included by all source files instantiating the design.
// The class here is then constructed to instantiate the design.
// See the Verilator manual for examples.

#ifndef VERILATED_VQ_WALL_GATE_H_
#define VERILATED_VQ_WALL_GATE_H_  // guard

#include "verilated.h"

class Vq_wall_gate__Syms;
class Vq_wall_gate___024root;

// This class is the main interface to the Verilated model
class alignas(VL_CACHE_LINE_BYTES) Vq_wall_gate VL_NOT_FINAL : public VerilatedModel {
  private:
    // Symbol table holding complete model state (owned by this class)
    Vq_wall_gate__Syms* const vlSymsp;

  public:

    // CONSTEXPR CAPABILITIES
    // Verilated with --trace?
    static constexpr bool traceCapable = false;

    // PORTS
    // The application code writes and reads these signals to
    // propagate new values into/out from the Verilated model.
    VL_IN8(&clk,0,0);
    VL_IN8(&rst_n,0,0);
    VL_IN8(&i_go,0,0);
    VL_OUT8(&o_running,0,0);
    VL_OUT8(&o_bail,0,0);
    VL_OUT8(&o_tval,0,0);
    VL_OUT8(&o_cflag,0,0);
    VL_OUT8(&o_nf,3,0);
    VL_OUT8(&o_gopen,0,0);
    VL_OUT8(&o_em_mask,6,0);
    VL_OUT16(&o_t,13,0);
    VL_IN(&i_seed,31,0);
    VL_OUTW(&o_em_pm,335,0,11);
    VL_OUTW(&o_em_e,335,0,11);
    VL_IN64(&i_lats,41,0);
    VL_OUT64(&o_resid,47,0);
    VL_OUT64(&o_events,47,0);
    VL_OUT64(&o_mass,47,0);
    VL_OUT64(&o_cancels,47,0);
    VL_OUT64(&o_chatter,47,0);
    VL_OUT64(&o_settles,47,0);
    VL_OUT64(&o_gopen_tot,47,0);
    VL_OUT64(&o_gcomp,47,0);

    // CELLS
    // Public to allow access to /* verilator public */ items.
    // Otherwise the application code can consider these internals.

    // Root instance pointer to allow access to model internals,
    // including inlined /* verilator public_flat_* */ items.
    Vq_wall_gate___024root* const rootp;

    // CONSTRUCTORS
    /// Construct the model; called by application code
    /// If contextp is null, then the model will use the default global context
    /// If name is "", then makes a wrapper with a
    /// single model invisible with respect to DPI scope names.
    explicit Vq_wall_gate(VerilatedContext* contextp, const char* name = "TOP");
    explicit Vq_wall_gate(const char* name = "TOP");
    /// Destroy the model; called (often implicitly) by application code
    virtual ~Vq_wall_gate();
  private:
    VL_UNCOPYABLE(Vq_wall_gate);  ///< Copying not allowed

  public:
    // API METHODS
    /// Evaluate the model.  Application must call when inputs change.
    void eval() { eval_step(); }
    /// Evaluate when calling multiple units/models per time step.
    void eval_step();
    /// Evaluate at end of a timestep for tracing, when using eval_step().
    /// Application must call after all eval() and before time changes.
    void eval_end_step() {}
    /// Simulation complete, run final blocks.  Application must call on completion.
    void final();
    /// Are there scheduled events to handle?
    bool eventsPending();
    /// Returns time at next time slot. Aborts if !eventsPending()
    uint64_t nextTimeSlot();
    /// Trace signals in the model; called by application code
    void trace(VerilatedTraceBaseC* tfp, int levels, int options = 0) { contextp()->trace(tfp, levels, options); }
    /// Retrieve name of this model instance (as passed to constructor).
    const char* name() const;

    // Abstract methods from VerilatedModel
    const char* hierName() const override final;
    const char* modelName() const override final;
    unsigned threads() const override final;
    /// Prepare for cloning the model at the process level (e.g. fork in Linux)
    /// Release necessary resources. Called before cloning.
    void prepareClone() const;
    /// Re-init after cloning the model at the process level (e.g. fork in Linux)
    /// Re-allocate necessary resources. Called after cloning.
    void atClone() const;
  private:
    // Internal functions - trace registration
    void traceBaseModel(VerilatedTraceBaseC* tfp, int levels, int options);
};

#endif  // guard
