# Verilated -*- Makefile -*-
# DESCRIPTION: Verilator output: Make include file with class lists
#
# This file lists generated Verilated files, for including in higher level makefiles.
# See Vq_fabric_top.mk for the caller.

### Switches...
# C11 constructs required?  0/1 (always on now)
VM_C11 = 1
# Timing enabled?  0/1
VM_TIMING = 0
# Coverage output mode?  0/1 (from --coverage)
VM_COVERAGE = 0
# Parallel builds?  0/1 (from --output-split)
VM_PARALLEL_BUILDS = 1
# Tracing output mode?  0/1 (from --trace/--trace-fst)
VM_TRACE = 0
# Tracing output mode in VCD format?  0/1 (from --trace)
VM_TRACE_VCD = 0
# Tracing output mode in FST format?  0/1 (from --trace-fst)
VM_TRACE_FST = 0

### Object file lists...
# Generated module classes, fast-path, compile with highest optimization
VM_CLASSES_FAST += \
	Vq_fabric_top \
	Vq_fabric_top___024root__DepSet_h2363dde7__0 \
	Vq_fabric_top___024root__DepSet_hdecc7538__0 \
	Vq_fabric_top_q_cell__DepSet_hd3f41de8__0 \
	Vq_fabric_top_q_cell__DepSet_hd3f41de8__1 \
	Vq_fabric_top_q_cell__DepSet_hd3f41de8__2 \
	Vq_fabric_top_q_cell__DepSet_hd3f41de8__3 \
	Vq_fabric_top_q_cell__DepSet_hd3f41de8__4 \
	Vq_fabric_top_q_cell__DepSet_hd3f41de8__5 \
	Vq_fabric_top_q_cell__DepSet_hd3f41de8__6 \
	Vq_fabric_top_q_cell__DepSet_hd3f41de8__7 \

# Generated module classes, non-fast-path, compile with low/medium optimization
VM_CLASSES_SLOW += \
	Vq_fabric_top___024root__Slow \
	Vq_fabric_top___024root__DepSet_h2363dde7__0__Slow \
	Vq_fabric_top___024root__DepSet_hdecc7538__0__Slow \
	Vq_fabric_top_q_cell__Slow \
	Vq_fabric_top_q_cell__DepSet_hd3f41de8__0__Slow \

# Generated support classes, fast-path, compile with highest optimization
VM_SUPPORT_FAST += \
	Vq_fabric_top__Dpi \

# Generated support classes, non-fast-path, compile with low/medium optimization
VM_SUPPORT_SLOW += \
	Vq_fabric_top__Syms \

# Global classes, need linked once per executable, fast-path, compile with highest optimization
VM_GLOBAL_FAST += \
	verilated \
	verilated_dpi \
	verilated_threads \

# Global classes, need linked once per executable, non-fast-path, compile with low/medium optimization
VM_GLOBAL_SLOW += \


# Verilated -*- Makefile -*-
