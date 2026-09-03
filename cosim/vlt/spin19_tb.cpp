// spin19_tb.cpp -- minimal verilator driver for q_wall_gate cosim.
// The RTL prints the trace itself (T/E/F lines, `ifndef SYNTHESIS);
// this driver just loads +seed/+lats and clocks until done.
// One fabric tick per clock; ~5k cycles per run.
#include <verilated.h>
#include "Vq_wall_gate.h"
#include <cstdio>
#include <cstring>
#include <cstdlib>

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    unsigned long seed = 1;
    unsigned long long lats = 0;
    for (int i = 1; i < argc; i++) {
        if (!strncmp(argv[i], "+seed=", 6)) {
            seed = strtoul(argv[i] + 6, nullptr, 10);
        } else if (!strncmp(argv[i], "+lats=", 6)) {
            lats = 0; int idx = 0; char* p = argv[i] + 6;
            while (*p && idx < 10) {
                lats |= (unsigned long long)strtoul(p, &p, 10) << (6 * idx);
                idx++;
                if (*p == ',') p++;
            }
        }
    }
    auto* top = new Vq_wall_gate;
    top->clk = 0; top->rst_n = 0; top->i_go = 0; top->i_seed = 0;
    top->i_lats = 0;
    for (int i = 0; i < 4; i++) { top->clk = !top->clk; top->eval(); }
    top->rst_n = 1;
    top->i_seed = seed; top->i_lats = lats; top->i_go = 1;
    top->clk = 1; top->eval();
    top->i_go = 0; top->clk = 0; top->eval();
    int guard = 0;
    while (top->o_running && guard++ < 20000) {
        top->clk = 1; top->eval();
        top->clk = 0; top->eval();
    }
    // two more edges: lets ST_DONE evaluate (prints the F line)
    top->clk = 1; top->eval();
    top->clk = 0; top->eval();
    delete top;
    return 0;
}
