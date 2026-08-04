.PHONY: all test golden waves clean

# Default target: Running 'make' runs golden model, runs sim, and launches waveform viewer
all: tb waves

# 1. Generate golden reference data & hex files
golden:
	@echo "===> Generating Golden Model Stimulus..."
	@python3 goldenModel/golden_model.py

# 2. Run Cocotb simulation (depends on 'golden' running first)
tb: golden
	@echo "===> Running RTL Simulation with Cocotb..."
	@PYTHONPATH=$(PWD) $(MAKE) -C RTL_Architecture -f Makefile

# 3. Launch waveform viewer (depends on 'tb' running first)
waves: tb
	@echo "===> Launching Surfer Waveform Viewer..."
	@$(MAKE) -C RTL_Architecture -f Makefile waves

# Cleanup build artifacts and generated files
clean:
	@echo "===> Cleaning build files..."
	@rm -f goldenModel/*.hex goldenModel/*.png goldenModel/*.txt
	@$(MAKE) -C RTL_Architecture -f Makefile clean