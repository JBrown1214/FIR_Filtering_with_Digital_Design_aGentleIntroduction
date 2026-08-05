import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer
from pylab import show
import sys
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parent.parent
GOLDEN_DIR = REPO_ROOT / "goldenModel"
from goldenModel.golden_model import plot_waves



@cocotb.test()
async def fir_filter_tb(dut):
    """Test FIR filter with hex stimulus and golden model comparison"""
    
    # 1. Start a 25 MHz clock (40 ns period)
    cocotb.start_soon(Clock(dut.clk, 40, unit="ns").start())


    # 2. Reset the DUT
    dut.rst_n.value = 0
    dut.data_in.value = 0
    await Timer(80, unit="ns")
    dut.rst_n.value = 1
    await RisingEdge(dut.clk)


    # 3. Load stimulus and golden outputs dynamically
    with open(GOLDEN_DIR / "data_messy_stimulus.hex", "r") as f:
        stimulus = [int(line.strip(), 16) for line in f if line.strip()]

    with open(GOLDEN_DIR / "data_expected_output.hex", "r") as f:
        golden = [int(line.strip(), 16) for line in f if line.strip()]

    # 3.5 Load coeff_regs
    with open(GOLDEN_DIR / "data_fir_coeffs.hex", "r") as f:
        fircoeffs = [int(line.strip(), 16) for line in f if line.strip()]
    for idx in range(24):
        dut.coeff_regs[idx].value = fircoeffs[idx]


    # 4. Drive inputs and collect outputs
    error_count = 0
    pipeline_delay = 24  # adjust to match your FIR filter's latency
    recieved_output = []

    for i, val in enumerate(stimulus):
        dut.data_in.value = val
        await RisingEdge(dut.clk) # Check output after pipeline latency


        actual = int(dut.data_out.value)
        recieved_output.append(actual)
        if i >= pipeline_delay:
            expected = golden[i - pipeline_delay]
            
            if actual != expected:
                cocotb.log.error(f"MISMATCH at sample {i}: Expected {hex(expected)}, Got {hex(actual)}")
                error_count += 1
            elif actual == expected:
                cocotb.log.error(f" ✅ MATCH at sample {i}: Expected {hex(expected)}, Got {hex(actual)}")

    assert error_count == 0, f"Test failed with {error_count} mismatches!"
    plot_waves(stimulus)
    plot_waves(recieved_output)
    show(block=True)
    

    cocotb.log.info("🎉 FIR Filter test passed cleanly!")