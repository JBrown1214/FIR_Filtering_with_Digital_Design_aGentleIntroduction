# Makefile


# Force Make to use MSYS2 Unix shell instead of CMD on Windows
SHELL := sh


# Bypass Cocotb version check bug for Verilator 5.048
COCOTB_VERILATOR_SKIP_VERSION_CHECK = 1
export COCOTB_VERILATOR_SKIP_VERSION_CHECK

# Force Python environment variables for Cocotb on Windows
export PYTHONPATH := C:/Users/johnn_erba506/Documents/Git/FIR_RTL/.venv/Lib/site-packages

# Simulator selection
SIM ?= verilator
TOPLEVEL_LANG ?= verilog

# Point Cocotb directly to the binary executable on Windows
VERILATOR = verilator_bin.exe

# Verilator args - enable waveform tracing & struct/array expansion
EXTRA_ARGS += --trace --trace-structs

# Use cocotb wave generation
WAVES = 1

# RTL sources
VERILOG_SOURCES += $(PWD)/fir_filter_top.sv

# Top-level module name
COCOTB_TOPLEVEL = fir_filter_top

# Python test module
COCOTB_TEST_MODULES = fir_filter_tb

# Custom build output folder
SIM_BUILD = sim_build

# include cocotb's make rules
include $(subst \,/,$(shell cocotb-config --makefiles))/Makefile.sim

waves:
	$(MAKE) WAVES=1
	surfer sim_build/dump.vcd &