# Verilog setup
SIM ?= verilator
TOPLEVEL_LANG ?= verilog

# RTL & Testbench Setup
VERILOG_SOURCES     += $(CURDIR)/fir_filter_top.sv
COCOTB_TOPLEVEL      = fir_filter_top
COCOTB_TEST_MODULES  = fir_filter_tb

# Waveform Tracing
EXTRA_ARGS += --trace --trace-structs
WAVES = 1

# Include Cocotb's built-in simulation rules
include $(shell cocotb-config --makefiles)/Makefile.sim

# Custom target for waveform viewing
.PHONY: waves
waves:
	surfer sim_build/dump.vcd &