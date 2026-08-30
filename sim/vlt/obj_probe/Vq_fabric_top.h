// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Primary model header
//
// This header should be included by all source files instantiating the design.
// The class here is then constructed to instantiate the design.
// See the Verilator manual for examples.

#ifndef VERILATED_VQ_FABRIC_TOP_H_
#define VERILATED_VQ_FABRIC_TOP_H_  // guard

#include "verilated.h"
#include "svdpi.h"

class Vq_fabric_top__Syms;
class Vq_fabric_top___024root;
class Vq_fabric_top_q_cell;


// This class is the main interface to the Verilated model
class alignas(VL_CACHE_LINE_BYTES) Vq_fabric_top VL_NOT_FINAL : public VerilatedModel {
  private:
    // Symbol table holding complete model state (owned by this class)
    Vq_fabric_top__Syms* const vlSymsp;

  public:

    // CONSTEXPR CAPABILITIES
    // Verilated with --trace?
    static constexpr bool traceCapable = false;

    // PORTS
    // The application code writes and reads these signals to
    // propagate new values into/out from the Verilated model.
    VL_IN8(&clk,0,0);
    VL_IN8(&rst_n,0,0);
    VL_IN8(&i_val,0,0);
    VL_OUT8(&o_rdy,0,0);
    VL_IN8(&i_op,2,0);
    VL_IN8(&i_src,3,0);
    VL_IN8(&i_dst,3,0);
    VL_OUT8(&o_val,0,0);
    VL_IN8(&i_rdy,0,0);
    VL_OUT8(&o_op,2,0);
    VL_OUT8(&o_src,3,0);
    VL_OUT8(&o_dst,3,0);
    VL_OUT8(&o_ovf,0,0);
    VL_IN16(&i_a0,15,0);
    VL_IN16(&i_a1,15,0);
    VL_IN16(&i_a2,15,0);
    VL_IN16(&i_dat,15,0);
    VL_OUT16(&o_a0,15,0);
    VL_OUT16(&o_a1,15,0);
    VL_OUT16(&o_a2,15,0);
    VL_OUT16(&o_dat,15,0);

    // CELLS
    // Public to allow access to /* verilator public */ items.
    // Otherwise the application code can consider these internals.
    Vq_fabric_top_q_cell* const __PVT__q_fabric_top__DOT__nodes__BRA__0__KET____DOT__conn0__DOT__u_cell;
    Vq_fabric_top_q_cell* const __PVT__q_fabric_top__DOT__nodes__BRA__1__KET____DOT__connc__DOT__u_cell;
    Vq_fabric_top_q_cell* const __PVT__q_fabric_top__DOT__nodes__BRA__2__KET____DOT__connc__DOT__u_cell;
    Vq_fabric_top_q_cell* const __PVT__q_fabric_top__DOT__nodes__BRA__3__KET____DOT__connc__DOT__u_cell;
    Vq_fabric_top_q_cell* const __PVT__q_fabric_top__DOT__nodes__BRA__4__KET____DOT__connc__DOT__u_cell;
    Vq_fabric_top_q_cell* const __PVT__q_fabric_top__DOT__nodes__BRA__5__KET____DOT__connc__DOT__u_cell;
    Vq_fabric_top_q_cell* const __PVT__q_fabric_top__DOT__nodes__BRA__6__KET____DOT__connc__DOT__u_cell;
    Vq_fabric_top_q_cell* const __PVT__q_fabric_top__DOT__nodes__BRA__7__KET____DOT__connc__DOT__u_cell;
    Vq_fabric_top_q_cell* const __PVT__q_fabric_top__DOT__nodes__BRA__8__KET____DOT__connc__DOT__u_cell;
    Vq_fabric_top_q_cell* const __PVT__q_fabric_top__DOT__nodes__BRA__9__KET____DOT__connc__DOT__u_cell;
    Vq_fabric_top_q_cell* const __PVT__q_fabric_top__DOT__nodes__BRA__10__KET____DOT__connc__DOT__u_cell;
    Vq_fabric_top_q_cell* const __PVT__q_fabric_top__DOT__nodes__BRA__11__KET____DOT__connc__DOT__u_cell;
    Vq_fabric_top_q_cell* const __PVT__q_fabric_top__DOT__nodes__BRA__12__KET____DOT__connc__DOT__u_cell;
    Vq_fabric_top_q_cell* const __PVT__q_fabric_top__DOT__nodes__BRA__13__KET____DOT__connc__DOT__u_cell;
    Vq_fabric_top_q_cell* const __PVT__q_fabric_top__DOT__nodes__BRA__14__KET____DOT__connc__DOT__u_cell;

    // Root instance pointer to allow access to model internals,
    // including inlined /* verilator public_flat_* */ items.
    Vq_fabric_top___024root* const rootp;

    // CONSTRUCTORS
    /// Construct the model; called by application code
    /// If contextp is null, then the model will use the default global context
    /// If name is "", then makes a wrapper with a
    /// single model invisible with respect to DPI scope names.
    explicit Vq_fabric_top(VerilatedContext* contextp, const char* name = "TOP");
    explicit Vq_fabric_top(const char* name = "TOP");
    /// Destroy the model; called (often implicitly) by application code
    virtual ~Vq_fabric_top();
  private:
    VL_UNCOPYABLE(Vq_fabric_top);  ///< Copying not allowed

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
