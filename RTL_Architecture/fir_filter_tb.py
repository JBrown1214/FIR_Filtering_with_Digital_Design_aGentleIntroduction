import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer

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

    # 3. Load stimulus and golden outputs with PURE PYTHON
    # (No readmemh, no relative-path issues!)
    with open("messy_stimulus.hex", "r") as f:
        stimulus = [int(line.strip(), 16) for line in f if line.strip()]

    with open("expected_output.hex", "r") as f:
        golden = [int(line.strip(), 16) for line in f if line.strip()]

    # 4. Drive inputs and collect outputs
    error_count = 0
    pipeline_delay = 4  # adjust to match your FIR filter's latency

    for i, val in enumerate(stimulus):
        dut.data_in.value = val
        await RisingEdge(dut.clk)

        # Check output after pipeline latency
        if i >= pipeline_delay:
            expected = golden[i - pipeline_delay]
            actual = int(dut.data_out.value)
            
            if actual != expected:
                cocotb.log.error(f"MISMATCH at sample {i}: Expected {hex(expected)}, Got {hex(actual)}")
                error_count += 1

    assert error_count == 0, f"Test failed with {error_count} mismatches!"
    cocotb.log.info("🎉 FIR Filter test passed cleanly!")