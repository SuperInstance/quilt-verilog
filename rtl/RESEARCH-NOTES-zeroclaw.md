# RESEARCH NOTES — ZeroClaw's first RTL sketches

**Status:** SKETCH ONLY — comment-form interfaces, not yet compiled.
Real code lands in `rtl/` only after the cross-review round, per the
competition rules. Companion to `proposals/zeroclaw/ARCHITECTURE.md`.

Conventions (from the math policy, §3 of the architecture entry):

- Verilog-2005 synthesizable subset. No `initial`, no `real`, no
  SystemVerilog. Testbenches excepted (they are not in rtl/).
- All widths are parameters. No module ever learns a width.
- Signedness declared per port; saturate never wrap; truncate inside
  pipelines, convergent-round at integrating boundaries.
- Async-assert / sync-deassert reset (`rst_n`), single clock.

---

## Sketch 1 — `zc_prim_hebb` (the Hebbian edge, log-compressed, power-law forgetting)

Formulae implemented (cited in ARCHITECTURE.md §2.1):

- potentiation: `W ← min(W+1, 2^WCNT-1)`
- reading:      `w = ln(1+W)` in u4.12  — via `e·ln2 + ln(m)`, m ∈ [1,2),
                32-entry piecewise-linear LUT (shared zc_math_lut)
- decay:        hyperbola `W(t) = W0/(1 + W0·t/P0)` realized as
                decrement-by-one when `age ≥ P0 >> 2·msb(W)` (floor 1)

```verilog
// =========================================================================
// zc_prim_hebb — SKETCH (comment-form; real code after cross-review)
// One Hebbian edge: co-activation counter W, age counter, log reading.
// Tiny fabric: instantiated per edge (W/age in FF).
// Big fabric: W/age live in link_table BRAM rows; this module is the
//             shared step engine that time-multiplexes over rows.
// =========================================================================
module zc_prim_hebb #(
    parameter WCNT        = 16,              // W counter width (u16)
    parameter ACNT        = 24,              // age counter width (u24)
    parameter DECAY_SHIFT = 20,              // log2(P0) — decay horizon
    parameter LUT_D       = 5                // ln-LUT address bits (32 entries)
) (
    input  wire                 clk,
    input  wire                 rst_n,        // async assert, sync deassert

    // --- co-activation event port (from link/effect decode) -------------
    input  wire                 pot_en,       // "fire together": W increments
    output wire                 pot_full,     // W saturated at max — view flag

    // --- tick port (from zc_tick_sched, broadcast) ----------------------
    input  wire                 tick_en,      // one scheduler pass

    // --- state (register-file style; becomes BRAM row fields on big fab)
    // (in sketch: inferred regs; in fabric these are the table columns)
    //   reg [WCNT-1:0] w_cnt;
    //   reg [ACNT-1:0] age;

    // --- reading port (on qm_view / gravity multiply) -------------------
    input  wire                 rd_en,        // request the ln(1+W) reading
    output reg  [15:0]          w_q412,       // u4.12: ln(1+W), [0, 11.09]
    output wire                 w_valid,

    // --- shared math-lut handshake (priority encoder + ln LUT owned
    //     by zc_math_lut; hebb issues msb/frac, gets back ln term) -------
    output wire [WCNT-1:0]      norm_arg,     // 1+W, normalized externally
    input  wire [15:0]          ln_term,      // u4.12 ln(m) + e*ln2 result
    input  wire                 ln_valid
);

    // Internal plan (comment-form):
    //
    // always @(posedge clk or negedge rst_n) begin
    //   if (!rst_n) begin
    //     w_cnt <= {WCNT{1'b0}};
    //     age   <= {ACNT{1'b0}};
    //   end else begin
    //     // --- potentiation (priority over decay; both same tick is OK) --
    //     if (pot_en && w_cnt != {WCNT{1'b1}})
    //       w_cnt <= w_cnt + 1'b1;
    //
    //     // --- power-law decay: decrement when age >= P0 >> 2*msb(W) ----
    //     //   msb(W)  = priority-encoded floor(log2 W), shared PE in
    //     //             zc_math_lut; shift is 2*msb(W), saturating >= 1.
    //     //   This integrates to dW/dt = -W^2/P0  =>  W(t)=W0/(1+W0*t/P0)
    //     //   — the hyperbolic (gamma=1) forgetting law. Staircase
    //     //   envelope, pointwise decay-rate error <= 2x (documented).
    //     if (tick_en && w_cnt != {WCNT{1'b0}}) begin
    //       if (age + 1'b1 >= decay_interval) begin   // decay_interval =
    //         w_cnt <= w_cnt - 1'b1;                  //   max(1, P0 >> 2*msb)
    //         age   <= {ACNT{1'b0}};
    //       end else begin
    //         age <= age + 1'b1;
    //       end
    //     end
    //   end
    // end
    //
    // Reading path: rd_en latches norm_arg = w_cnt + 1; one round trip
    // through the shared normalize+LUT+ln2-shiftadd; w_q412 holds
    // u4.12 result, w_valid pulses. No per-edge LUT — shared by bank.

endmodule
```

Open questions for cross-review (flagged inline):

1. Should potentiation reset `age`? (Sketch says no: recent fire
   shouldn't pause forgetting of *older* association — but this is a
   doctrine call, not a math call. The C reference has no analog.)
2. `decay_interval` combinational (`PE + double shift + compare`) sits
   on the tick path per edge — fine per-edge, needs pipelining when
   time-multiplexed over BRAM rows on big fabric.

---

## Sketch 2 — `zc_prim_vmf` (streaming vMF: S, N → ρ, μ̂, κ̂)

Formulae implemented (ARCHITECTURE.md §2.2, after elephant
`contrast.py:vmf_fit_generic` + Sra 2012):

- accumulate: `S ← S + x`, `N ← N + 1` (x normalized at ingress)
- readout: `ρ = ‖S‖/N` [u0.15], `μ̂ = S/‖S‖` [s1.14],
  `κ̂ ≈ (ρ·D − ρ³)/(1 − ρ²)` [u7.8, saturate + clip flag]

```verilog
// =========================================================================
// zc_prim_vmf — SKETCH (comment-form; real code after cross-review)
// Streaming von Mises–Fisher estimator over D-dim unit vectors.
// D=8: dial bank, per-sample. D=64: wide fabric, MAC time-multiplexed.
// Sqrt/reciprocal shared via zc_math_lut (Newton–Raphson, 2 iter).
// =========================================================================
module zc_prim_vmf #(
    parameter D       = 8,          // vector dimension (dial bank native)
    parameter N_W     = 32,         // sample counter width
    parameter ACC_W   = 16 + 3      // s(A).14 accumulator width: 2 guard
                                    // bits + ceil(log2 N) via load-time widen
) (
    input  wire                 clk,
    input  wire                 rst_n,

    // --- sample ingress (already normalized: s1.14 components) ----------
    input  wire                 x_valid,
    output wire                 x_ready,      // backpressure; never drop
    input  wire signed [15:0]   x_comp,       // one component per beat,
                                              // D beats per sample (last flag
                                              // comes in on chan sideband in
                                              // the real stream wrapper)

    // --- readout (qm_view or per-tick dial-bank snapshot) ---------------
    input  wire                 rd_en,
    output reg  [14:0]          rho_q015,     // u0.15  ‖S‖/N
    output reg  signed [15:0]   mu_comp,      // s1.14  S_i/‖S‖, streamed D beats
    output reg  [15:0]          kappa_q78,    // u7.8   Sra approx, saturated
    output wire                 kappa_clip,   // ρ too close to 1 — do not trust
    output reg  [N_W-1:0]       n_count,      // exposed: small-N skepticism
    output wire                 rd_valid
);

    // Internal plan (comment-form):
    //
    // state:  acc [D][ACC_W-1:0] signed;  n [N_W-1:0]
    // sample: for i in 0..D-1 (x_valid beats): acc[i] <= sat(acc[i] + x_comp)
    //         n <= n + 1   (convergent round NOT needed on add — integer N,
    //         s1.14 adds into wider accumulator; guard bits per policy)
    //
    // readout pipeline (multi-cycle, one round trip through zc_math_lut):
    //   1. sq = Σ acc[i]^2          (time-mux MAC, s(2+ceil(log2 D)+...).14)
    //   2. r   = sqrt(sq)           (NR unit)          -> ‖S‖
    //   3. recip = 1/r              (same NR unit)     -> shared 1/‖S‖
    //   4. rho   = (r * recip_N) >> ...                -> u0.15, convergent
    //      round at this boundary (integrating output)
    //   5. mu_i  = acc[i] * recip                    -> s1.14, conv. round
    //   6. kappa = (rho*D - rho^3) / (1 - rho^2)      -> u7.8
    //      implemented as: num = rho*D - rho^3 (u?), den = (1-rho)*(1+rho)
    //      via shared reciprocal; saturate at KAPPA_MAX, raise kappa_clip
    //      when rho > RHO_TRUST (0.95 default) — TB asserts vs real
    //      bisection on A_d(kappa)=rho (the contrast.py golden).

    // Honesty note carried in ports: n_count is a first-class output.
    // At small N the rho reading is biased low (sqrt(N/D) floor, per
    // elephant contrast.py) — consumers must be able to disbelieve.

endmodule
```

Open questions for cross-review:

1. Accumulator load-time widening vs fixed ACC_W with saturation —
   fixed width is simpler; policy §3.2 says saturate, but saturating
   the *sum* silently biases ρ. Proposal: saturate + expose an
   `acc_clip` flag alongside `kappa_clip`. Review should decide.
2. Is D beats-per-sample component streaming the right ingress shape,
   or should components arrive as full parallel D-wide words on big
   fabric (parameterizing a wrapper, not the core)?

---

*Next step: cross-review round. Code lands only in what survives.*
