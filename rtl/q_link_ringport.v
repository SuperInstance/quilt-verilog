// q_link_ringport.v -- one ring node: deliver / transit / inject.
// Pure comb (opencode RTL-SKETCH §1, reused per scorecard steal 3 advice:
// "skeletons compile clean, correct ready logic"). Registered slices
// (q_flit_pipe) are inserted by fabric_top for timing; ports identical.
// Single-ring liveness: transit never blocks unless downstream blocks;
// delivery consumes the slot and frees a bubble for injection.
module q_link_ringport #(
    parameter OPW  = 3,
    parameter AIDW = 4,
    parameter PW   = 16
)(
    input  wire [AIDW-1:0]    i_myid,

    input  wire               ri_valid,
    output wire               ri_ready,
    input  wire [OPW-1:0]     ri_op,
    input  wire [AIDW-1:0]    ri_src,
    input  wire [AIDW-1:0]    ri_dst,
    input  wire [PW-1:0]      ri_a0,
    input  wire [PW-1:0]      ri_a1,
    input  wire [PW-1:0]      ri_a2,
    input  wire [PW-1:0]      ri_dat,

    output wire               ro_valid,
    input  wire               ro_ready,
    output wire [OPW-1:0]     ro_op,
    output wire [AIDW-1:0]    ro_src,
    output wire [AIDW-1:0]    ro_dst,
    output wire [PW-1:0]      ro_a0,
    output wire [PW-1:0]      ro_a1,
    output wire [PW-1:0]      ro_a2,
    output wire [PW-1:0]      ro_dat,

    input  wire               li_valid,
    output wire               li_ready,
    input  wire [OPW-1:0]     li_op,
    input  wire [AIDW-1:0]    li_src,
    input  wire [AIDW-1:0]    li_dst,
    input  wire [PW-1:0]      li_a0,
    input  wire [PW-1:0]      li_a1,
    input  wire [PW-1:0]      li_a2,
    input  wire [PW-1:0]      li_dat,

    output wire               ld_valid,
    input  wire               ld_ready,
    output wire [OPW-1:0]     ld_op,
    output wire [AIDW-1:0]    ld_src,
    output wire [AIDW-1:0]    ld_dst,
    output wire [PW-1:0]      ld_a0,
    output wire [PW-1:0]      ld_a1,
    output wire [PW-1:0]      ld_a2,
    output wire [PW-1:0]      ld_dat
);
    wire hit       = ri_valid && (ri_dst == i_myid);
    wire consumed  = hit && ld_ready;
    wire transit   = ri_valid && !consumed;
    wire inject_ok = !ri_valid || consumed;

    assign ld_valid = hit;
    assign ld_op    = ri_op;
    assign ld_src   = ri_src;
    assign ld_dst   = ri_dst;
    assign ld_a0    = ri_a0;
    assign ld_a1    = ri_a1;
    assign ld_a2    = ri_a2;
    assign ld_dat   = ri_dat;

    assign ro_valid = transit || (li_valid && inject_ok);
    assign ro_op    = transit ? ri_op  : li_op;
    assign ro_src   = transit ? ri_src : li_src;
    assign ro_dst   = transit ? ri_dst : li_dst;
    assign ro_a0    = transit ? ri_a0  : li_a0;
    assign ro_a1    = transit ? ri_a1  : li_a1;
    assign ro_a2    = transit ? ri_a2  : li_a2;
    assign ro_dat   = transit ? ri_dat : li_dat;

    assign ri_ready = hit ? ld_ready : ro_ready;
    assign li_ready = inject_ok && ro_ready;

endmodule
