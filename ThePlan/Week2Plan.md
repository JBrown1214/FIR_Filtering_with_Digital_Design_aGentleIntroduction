# Week 2: The Core FIR Architecture & Hardware Verification

**Time Budget:** 12 Hours
**Primary Objective:** Translate your discrete-time mathematical model into a synthesizable, clocked digital logic pipeline in Verilog. Once built, you will simulate the hardware, feed it the stimulus file from Week 1, and prove the hardware output perfectly matches your Python Golden Model.

---

## Work Block 1: The Delay Line (2 Hours)
In hardware, the $x[n-k]$ portion of the FIR equation is a shift register. Every clock cycle, a new 16-bit sample enters, and all older samples shift down the chain.

* **Execution:**
  1. Create your primary Verilog module: `fir_filter.v`. 
  2. Define the inputs: `clk`, `reset_n` (active low), `data_in` (16-bit signed), and `data_valid_in` (a control signal to tell the filter when incoming data is good).
  3. Define the output: `data_out` (16-bit signed) and `data_valid_out`.
  4. Create a 2D packed array for the shift register. If you are using a 15-tap filter, you need an array of fifteen 16-bit registers.
  5. Write the sequential logic block (`always @(posedge clk)`) that shifts the data down the array by one index every time `data_valid_in` is high.

## Work Block 2: The Pipelined MAC Engine (4 Hours)
This is where you earn the interview. A standard software engineer might try to multiply and add all 15 taps in a single line of code. In hardware, that creates a massive combinational logic path that will destroy your maximum clock frequency ($F_{max}$). You must pipeline the math.

* **Execution:**
  1. **Stage 1 (Multiplication):** Create a new array of fifteen 32-bit registers. On the clock edge, multiply each value in the delay line by its corresponding fixed-point coefficient and store it in this new array. (For now, you can hardcode the coefficients initialized from your `fir_coeffs.hex` file using `initial $readmemh`; you will make them dynamic via SPI in Week 4).
  2. **Truncation:** Right-shift the 32-bit results by 15 (`>> 15`) to bring them back to 16-bit Q1.15 format before passing them to the adders. 
  3. **Stage 2+ (The Adder Tree):** Do not add all 15 numbers at once. Build an adder tree. Add pairs of numbers together and store them in a new register stage. Then add those results together in the next clock cycle.
  4. **Latency Tracking:** Because of pipelining, it will take several clock cycles for a sample to emerge from the filter. Use a shift register to delay the `data_valid_in` signal by the exact number of pipeline stages, outputting it as `data_valid_out`.

## Work Block 3: The Comprehensive Testbench (4 Hours)
An FPGA design is completely useless without a testbench to prove it works. You will use the files you generated in Week 1 to simulate a real-world data stream.

* **Execution:**
  1. Create `tb_fir.v`.
  2. Instantiate your `fir_filter` module.
  3. Generate a clock signal (e.g., toggling a register every 20ns to simulate a 25 MHz clock).
  4. **File Input:** Use the Verilog `$readmemh` system task to load `stimulus.hex` into a memory array inside the testbench.
  5. **Data Streaming:** Write a loop that feeds one value from the memory array into the `data_in` port of your filter every clock cycle, toggling `data_valid_in` high.
  6. **File Output:** Use `$fopen` to create `verilog_output.hex`. Whenever `data_valid_out` is high, use `$fdisplay` to write the filter's `data_out` to this text file.

## Work Block 4: Verification & Sign-off (2 Hours)
You now have the output from your hardware simulation. It is time to see if it matches reality.

* **Execution:**
  1. Run the testbench in ModelSim, Gowin Simulator, or Icarus Verilog.
  2. Open the waveform viewer. Visually confirm that data is shifting through the pipeline and that the valid signals are aligning correctly.
  3. Write a quick Python script (`verify_hardware.py`) that opens both `expected_output.hex` (from Week 1) and `verilog_output.hex` (from today).
  4. Compare the two arrays. *Note: They might be offset by a few indices due to the pipeline latency of your Verilog module. Account for this shift in your script.*
  5. If the arrays match perfectly (or within a margin of $\pm 1$ due to slight rounding differences), your core DSP engine is complete.

---

## Week 2 Deliverables Checklist
Before moving on to the noise generator and BRAM in Week 3, ensure you have:
* [ ] `fir_filter.v` (The pipelined hardware module)
* [ ] `tb_fir.v` (The simulation environment reading/writing hex files)
* [ ] `verilog_output.hex` (The captured hardware simulation data)
* [ ] A screenshot of the simulation waveforms showing the pipelined delays.
* [ ] Confirmation that the Verilog output mathematically matches the Python Golden Model.