// q_wall_gate.v -- SPIN-19 RTL-HONESTY: the wheel's pulse-dial fabric
// (spin11.run_fabric_mc / spin16.run_fabric_gate, "interference" mode)
// as one cycle-per-tick integer RTL cell. Bit-exact co-simulation
// target: every observable (events, mass, cancels, chatter, settles,
// resid/cflag traces, emission list, gopen/gcomp) must match the Python
// model exactly (WHEEL-LOG SPIN-16). Verilog-2005, parameterized
// integer style (zeroclaw rule 6: integer state, never fixed-point,
// never drifts).
//
// MODEL (Python reference, one fabric tick t):
//   reads[i] = reality(max(0,t-lat_i)); s_true = reality(t)
//   g += LCG.below(13) - 6                  (drift=6; LCG stepped once/tick)
//   pop pulses with life 0; guard (modes 1/2): any |e_i|>1e12 ->
//       resid, cflag=0, halt (nothing else counted that tick)
//   trig = { i : |reads_i - g| > delta };  nf = |trig|
//   gate: open = nf>0 and 100*|pd-nf| > theta100*pd   (theta mode; the
//         echo factor |1-nf/pd|>theta precomputed by cross-multiplication
//         -- no division in the gate path)
//   neff = always: min(nf,pd) / theta: open?min(nf,pd):(nf?1:0) /
//          never: nf?1:0
//   per trig: m = |e|/pd or 1; if neff>1: m = m/neff or 1; pm = +/-m
//             pulse born (pm, life=K)
//   net = sum all live mags; cancels++ if net==0 and +/- both present
//   g += net; decay every live mag: m = (|m|>1)? ceil(m/2) : m; life--
//   chatter/last on trig; settles if all |reads_i-g| <= delta
//   resid_t = |s_true - g|; cflag_t
//
// PULSE STORAGE: all pulses decay in lockstep, so live cohorts are ages
// 0..K-1 -- a K-slot circular bank indexed by birth tick mod K. At tick
// t slot t%K is overwritten by the new cohort (this simultaneously
// retires the age-K cohort, which Python pops before net). Registers
// hold the value each cohort contributes at the CURRENT tick (decay is
// applied post-net), so net = fresh cohort + sum(stored slots).
//
// GMODE: 0 = "never"  (neff=1, == spin11 mc=0, no memory guard)
//        1 = "always" (neff=min(nf,pd), == spin11 mc=1 / MC-A)
//        2 = theta    (echo gate; THETA100 = round(100*theta))
module q_wall_gate #(
    parameter N        = 7,     // sensor twins
    parameter K        = 1,     // pulse life (ticks)
    parameter PD       = 3,     // pulse dial
    parameter DELTA    = 12,    // trigger threshold
    parameter DRIFT    = 6,     // drift amplitude (below(2*DRIFT+1)-DRIFT)
    parameter PW       = 48,    // integer datapath width (signed)
    parameter TW       = 14,    // tick counter width
    parameter LSW      = 6,     // latency field width
    parameter GMODE    = 2,     // 0 never / 1 always / 2 theta
    parameter [7:0] THETA100 = 8'd110, // round(100*theta); theta=1.1
    parameter TICKS    = 4800
)(
    input  wire                  clk,
    input  wire                  rst_n,
    input  wire                  i_go,
    input  wire [31:0]           i_seed,
    input  wire [N*LSW-1:0]      i_lats,

    output reg                   o_running,
    output reg                   o_bail,     // memory guard tripped
    output reg  [TW-1:0]         o_t,
    output reg  [PW-1:0]         o_resid,    // |s_true - g|, valid at o_tval
    output reg                   o_tval,
    output reg                   o_cflag,
    output reg  [3:0]            o_nf,
    output reg                   o_gopen,    // this tick's gate-open strobe
    output reg  [N-1:0]          o_em_mask,  // emission strobes (index order)
    output reg  [N*PW-1:0]       o_em_pm,    // signed pulse mags, packed
    output reg  [N*PW-1:0]       o_em_e,     // signed raw errors, packed
    output reg  [PW-1:0]         o_events,
    output reg  [PW-1:0]         o_mass,
    output reg  [PW-1:0]         o_cancels,
    output reg  [PW-1:0]         o_chatter,
    output reg  [PW-1:0]         o_settles,
    output reg  [PW-1:0]         o_gopen_tot,
    output reg  [PW-1:0]         o_gcomp
);
    localparam signed [PW-1:0] GUARD = 48'd1000000000000;

    // ------------------------------------------------------------ helpers
    function signed [PW-1:0] f_reality;
        input [TW-1:0] ph;                  // phase = t % 240 (0..239)
        begin
            if (ph < 96)       f_reality = 400 + (ph * 8) / 5;
            else if (ph < 144) f_reality = 553 - (ph - 96);
            else               f_reality = 505 - ((ph - 144) * 8) / 5;
        end
    endfunction

    function signed [PW-1:0] f_abs;
        input signed [PW-1:0] v;
        begin
            f_abs = (v < 0) ? -v : v;
        end
    endfunction

    // ------------------------------------------------------------ state
    reg [31:0]          lcg_x;                  // pre-step LCG state
    reg signed [PW-1:0] g;                      // post-net g (prev tick)
    reg signed [TW:0]   t;
    reg signed [PW-1:0] mags [0:K-1][0:N-1];    // cohort slot, member
    reg [3:0]           cnt  [0:K-1];
    reg signed [TW:0]   last;                   // last fire tick, init -10
    reg [1:0]           st;
    localparam ST_IDLE = 2'd0, ST_RUN = 2'd1, ST_DONE = 2'd2;

    reg [LSW-1:0] i_lats_reg [0:N-1];

    // per-tick combinational
    reg signed [PW-1:0] reads [0:N-1];
    reg signed [PW-1:0] errs  [0:N-1];
    reg [N-1:0]      trig;
    reg [3:0]        nf;
    reg signed [PW-1:0] pm_new [0:N-1];
    reg [3:0]        neff;
    reg              open_;
    reg signed [PW-1:0] net, g_now, s_true;
    reg              any_pos, any_neg, cancel, guard_hit;
    reg signed [PW-1:0] mtmp;
    reg [TW-1:0]     eff, ph;
    integer ii, jj, kk, q;
    reg              sall;
    reg [31:0]       lcg_next;
    reg signed [PW-1:0] drift_val;
    reg [63:0]       lprod;

    // LCG: x = (1103515245*x + 12345) & 0x7fffffff, drift = x % 13 - 6
    always @* begin
        lprod    = 64'd1103515245 * lcg_x + 64'd12345;
        lcg_next = lprod[30:0];
        drift_val = $signed({{PW-31{1'b0}}, lcg_next % 13}) - DRIFT;
        g_now = g + drift_val;               // drift applied this tick
    end

    // ------------------------------------------------------------ datapath
    always @* begin
        ph        = t % 240;
        s_true    = f_reality(ph);
        guard_hit = 1'b0;
        trig      = {N{1'b0}};
        nf        = 4'd0;
        neff      = 4'd0;
        open_     = 1'b0;
        net       = {PW{1'b0}};
        any_pos   = 1'b0;
        any_neg   = 1'b0;
        cancel    = 1'b0;

        for (ii = 0; ii < N; ii = ii + 1) begin
            eff = (t >= $signed({1'b0, i_lats_reg[ii]}))
                  ? t - $signed({1'b0, i_lats_reg[ii]}) : 0;
            reads[ii] = f_reality(eff % 240);
            errs[ii]  = reads[ii] - g_now;
            if (f_abs(errs[ii]) > GUARD) guard_hit = 1'b1;
            if (f_abs(errs[ii]) > DELTA) trig[ii]  = 1'b1;
        end
        for (ii = 0; ii < N; ii = ii + 1)
            if (trig[ii]) nf = nf + 4'd1;

        // echo gate: |1 - nf/pd| > theta  <=>  100*|pd-nf| > theta100*pd
        // (multiplication only -- no division in the gate path)
        if (GMODE == 2)
            open_ = (nf != 0) &&
                    ((PD > nf) ? 100 * (PD - nf) : 100 * (nf - PD))
                    > THETA100 * PD;

        if (GMODE == 1)
            neff = (nf > PD) ? PD : nf;
        else if (GMODE == 2)
            neff = open_ ? ((nf > PD) ? PD : nf) : ((nf != 0) ? 4'd1 : 4'd0);
        else
            neff = (nf != 0) ? 4'd1 : 4'd0;

        for (ii = 0; ii < N; ii = ii + 1) begin
            pm_new[ii] = {PW{1'b0}};
            if (trig[ii]) begin
                mtmp = f_abs(errs[ii]) / PD;
                if (mtmp == 0) mtmp = 1;
                if (neff > 1) begin
                    mtmp = mtmp / neff;
                    if (mtmp == 0) mtmp = 1;
                end
                pm_new[ii] = (errs[ii] > 0) ? mtmp : -mtmp;
            end
        end

        // net: fresh cohort (slot t%K) + all other stored slots. The
        // stored copy of slot t%K holds the retiring age-K cohort,
        // which Python pops before net -- replaced, hence excluded.
        for (kk = 0; kk < K; kk = kk + 1)
            for (jj = 0; jj < N; jj = jj + 1) begin
                if (kk == (t % K)) begin
                    if (trig[jj]) begin
                        net = net + pm_new[jj];
                        if (pm_new[jj] > 0) any_pos = 1'b1;
                        if (pm_new[jj] < 0) any_neg = 1'b1;
                    end
                end else if (jj < cnt[kk]) begin
                    net = net + mags[kk][jj];
                    if (mags[kk][jj] > 0) any_pos = 1'b1;
                    if (mags[kk][jj] < 0) any_neg = 1'b1;
                end
            end
        cancel = (net == 0) && any_pos && any_neg;
    end

    // ------------------------------------------------------------ sequencer
    integer a, b;
    reg signed [PW-1:0] dv;
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            st <= ST_IDLE; o_running <= 1'b0; o_bail <= 1'b0;
            o_tval <= 1'b0; o_gopen <= 1'b0; o_em_mask <= {N{1'b0}};
            o_events <= 0; o_mass <= 0; o_cancels <= 0; o_chatter <= 0;
            o_settles <= 0; o_gopen_tot <= 0; o_gcomp <= 0;
        end else begin
            o_tval    <= 1'b0;
            o_gopen   <= 1'b0;
            o_em_mask <= {N{1'b0}};
            case (st)
              ST_IDLE: if (i_go) begin
                  // Python: x = seed & 0x7fffffff or 1  (falsy -> 1)
                  if ((i_seed & 32'h7fffffff) == 0) lcg_x <= 32'h1;
                  else                              lcg_x <= i_seed & 32'h7fffffff;
                  g    <= 400;                     // reality(0)
                  t    <= 0;
                  last <= -10;
                  for (a = 0; a < K; a = a + 1) begin
                      cnt[a] <= 4'd0;
                      for (b = 0; b < N; b = b + 1)
                          mags[a][b] <= {PW{1'b0}};
                  end
                  for (a = 0; a < N; a = a + 1)
                      i_lats_reg[a] <= i_lats[a*LSW +: LSW];
                  o_events <= 0; o_mass <= 0; o_cancels <= 0;
                  o_chatter <= 0; o_settles <= 0;
                  o_gopen_tot <= 0; o_gcomp <= 0; o_bail <= 1'b0;
                  st <= ST_RUN; o_running <= 1'b1;
              end
              ST_RUN: begin
                  lcg_x <= lcg_next;               // one step per tick
                  o_t   <= t[TW-1:0];
                  o_tval<= 1'b1;
                  o_nf  <= nf;
`ifndef SYNTHESIS
                  // co-sim trace (verilator): one T line per tick, one E
                  // line per emission in index order, F line at the end.
                  if ((GMODE != 0) && guard_hit)
                      $display("T %0d %0d %0d %0d %0d", t,
                               f_abs(s_true - g_now), 0, 0, 0);
                  else begin
                      $display("T %0d %0d %0d %0d %0d", t,
                               f_abs(s_true - (g_now + net)), cancel, nf,
                               open_);
                      for (a = 0; a < N; a = a + 1)
                          if (trig[a])
                              $display("E %0d %0d %0d %0d", t, a,
                                       pm_new[a], errs[a]);
                  end
`endif

                  if ((GMODE != 0) && guard_hit) begin
                      // memory guard: resid, cflag 0, halt. Python breaks
                      // after appending this tick's resid only; drift WAS
                      // applied, net was not; no counters move.
                      o_resid  <= f_abs(s_true - g_now);
                      o_cflag  <= 1'b0;
                      g        <= g_now;
                      o_bail   <= 1'b1;
                      st       <= ST_DONE;
                      o_running<= 1'b0;
                  end else begin
                      for (a = 0; a < N; a = a + 1) begin
                          o_em_pm[a*PW +: PW] <= pm_new[a];
                          o_em_e[a*PW +: PW]  <= errs[a];
                      end
                      o_em_mask <= trig;
                      o_gopen   <= open_;
                      o_cflag   <= cancel;
                      o_resid   <= f_abs(s_true - (g_now + net));

                      // retire + write slot t%K with the fresh cohort
                      cnt[t % K] <= nf;
                      for (a = 0; a < N; a = a + 1)
                          mags[t % K][a] <= pm_new[a];

                      if (nf != 0) begin
                          o_events <= o_events + nf;
                          for (a = 0; a < N; a = a + 1)
                              if (trig[a]) o_mass <= o_mass + f_abs(errs[a]);
                          if (neff > 1) o_gcomp <= o_gcomp + nf;
                          if (open_)    o_gopen_tot <= o_gopen_tot + 1;
                          if (t == last + 1) o_chatter <= o_chatter + 1;
                          last <= t;
                      end
                      if (cancel) o_cancels <= o_cancels + 1;

                      // net applied to g (Python applies only if pulses
                      // exist; pulses empty forces net==0, so exact)
                      g <= g_now + net;

                      // decay all live mags: (|m|>1) ? ceil(m/2) : m.
                      // Slot t%K gets the FRESH values decayed (Python
                      // decays a newborn pulse in its birth tick).
                      for (a = 0; a < K; a = a + 1)
                          for (b = 0; b < N; b = b + 1) begin
                              dv = (a == (t % K)) ? pm_new[b] : mags[a][b];
                              if (f_abs(dv) > 1) mags[a][b] <= (dv + 1) >>> 1;
                              else               mags[a][b] <= dv;
                          end

                      // settles: all |reads_i - g'| <= delta
                      sall = 1'b1;
                      for (q = 0; q < N; q = q + 1)
                          if (f_abs(reads[q] - (g_now + net)) > DELTA)
                              sall = 1'b0;
                      if (sall) o_settles <= o_settles + 1;

                      if (t == TICKS - 1) begin
                          st <= ST_DONE;
                          o_running <= 1'b0;
                      end else begin
                          t <= t + 1;
                      end
                  end
              end
              ST_DONE: begin
                  o_running <= 1'b0;
`ifndef SYNTHESIS
                  $display("F %0d %0d %0d %0d %0d %0d %0d %0d", o_events,
                           o_mass, o_cancels, o_chatter, o_settles,
                           o_gopen_tot, o_gcomp, o_bail);
`endif
              end
              default: st <= ST_IDLE;
            endcase
        end
    end
endmodule
