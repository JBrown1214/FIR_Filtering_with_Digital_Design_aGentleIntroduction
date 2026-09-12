import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer
import sys
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parent.parent
GOLDEN_DIR = REPO_ROOT / "goldenModel"
from goldenModel.golden_model import plot_waves, plot_delta_histogram, FIR_filter
from goldenModel.qFormat_conversions import qFormat_to_float, float_to_qFormat, lossy_conversion
import matplotlib.pyplot as plt


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

    stimulus_float = []
    for i in range(len(stimulus)):
        stimulus_float.append(qFormat_to_float(stimulus[i]))

    with open(GOLDEN_DIR / "data_expected_output.hex", "r") as f:
        golden = [int(line.strip(), 16) for line in f if line.strip()]

    golden_float = []
    for i in range(len(golden)):
        golden_float.append(qFormat_to_float(golden[i]))

    # 3.5 Load coeff_regs
    with open(GOLDEN_DIR / "data_fir_coeffs.hex", "r") as f:
        fircoeffs = [int(line.strip(), 16) for line in f if line.strip()]
    for idx in range(24):
        dut.coeff_regs[idx].value = fircoeffs[idx]


    # 4. Drive inputs and collect outputs
    error_count = 0
    pipeline_delay = 9  # adjust to match your FIR filter's latency
    recieved_output = []
    recieved_output_float = []

    deltas = []
    delta_L = [.1,9999999]
    delta_S = [1000,0]
    delta_count = {}
    weird_deltas = {}

    for i, val in enumerate(stimulus):
        dut.data_in.value = val
        await RisingEdge(dut.clk) # Check output after pipeline latency


        actual = int(dut.data_out.value)
        recieved_output.append(actual)
        recieved_output_float.append(qFormat_to_float(actual))
        if i >= pipeline_delay:
            expected = golden[i - pipeline_delay]
            delta = abs(actual - expected)
            delta_count[delta] = delta_count.get(delta, 0) + 1

            if actual != expected:
                deltas.append(delta)

                # Largest/Smallest delta logic
                if abs(delta) < abs(delta_S[0]):
                    delta_S[0] = delta
                    delta_S[1] = i
                elif abs(delta) > abs(delta_L[0])and (abs(qFormat_to_float(delta)) > 2**-14):
                    delta_L[0] = delta
                    delta_L[1] = i
                # "weird_delta" logic (abnormal from the "low teens" trend)
                if abs(delta) > 32 and (abs(qFormat_to_float(delta)) > 2**-13):  # catch small negative mismatches that present as deltas of 64000
                    weird_deltas[i] = delta
                if abs(delta) < 5:
                    weird_deltas[i] = delta

                # print mismatch to console
                cocotb.log.error(f"MISMATCH at sample {i}: Expected {hex(expected)}, Got {hex(actual)}, Delta {delta} = {hex(delta)}")
                error_count += 1
            elif actual == expected:
                deltas.append(delta)

                cocotb.log.info(f" ✅ MATCH at sample {i}: Expected {hex(expected)}, Got {hex(actual)}")


    ##=========================================================================================
    ##================== Delta between golden model and SystemVerilog Model ===================
    ##=========================================================================================

    # deltas_float = []
    # for i in range(len(deltas)):
    #     if deltas[i] < 0:
    #         deltas_float.append(qFormat_to_float(deltas[i] + 0x1111))
    #     else:
    #         deltas_float.append(qFormat_to_float(deltas[i]))

    # print(f"Largest delta is {delta_L[0]} at sample {delta_L[1]}")
    # print(f"Smallest delta is {delta_S[0]} at sample {delta_S[1]}")
    # print(f"WEIRD deltas \n {weird_deltas}")
    # print()
    # print(f"Delta Count \n {delta_count}")
    # print()
    # print(f"Deltas \n {deltas[:20]}")
    # print()
    # print(f"Deltas_float\n {deltas_float[:20]}")
    # print()

    # plot_delta_histogram(delta_count)
    # plot_waves(deltas_float, seed="deltas_plot_", dynamic_ylims=True)




    # plot_waves(list(stimulus_float), seed="tb_plot_Stimulus_")
    # plot_waves(golden_float, seed="tb_plot_goldenOUT_")
    # plot_waves(recieved_output_float, seed="tb_plot_VerilogOUT_")
    # plot_waves(golden_float, recieved_output_float, seed="tb_plot_overlayOUT_", overlay=True)

    assert error_count == 0, f"Test failed with {error_count} mismatches!"

    cocotb.log.info("🎉 FIR Filter test passed cleanly!")