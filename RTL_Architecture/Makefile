# ==============================================================================
# SYSTEMVERILOG FIR FILTER SIMULATION MAKEFILE
# ==============================================================================

SIM ?= verilator
TOPLEVEL_LANG ?= verilog

# RTL & Testbench Setup
VERILOG_SOURCES     += $(CURDIR)/fir_filter_top.sv
COCOTB_TOPLEVEL      = fir_filter_top
COCOTB_TEST_MODULES  = fir_filter_tb

# Waveform Tracing
EXTRA_ARGS += --trace --trace-structs
WAVES = 1

# New (Cocotb 2.0+):
include $(shell cocotb-config --makefiles)/Makefile.sim


# Custom Targets
.PHONY: waves clean_all

waves:
	$(MAKE) WAVES=1
	surfer sim_build/dump.vcd &

clean_all:
	rm -rf sim_build results.xml *.vcd