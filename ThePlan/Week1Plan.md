# Week 1: Fixed-Point Math & The Python Golden Model

**Time Budget:** 10 Hours
**Primary Objective:** Establish the mathematical ground truth. Hardware debugging is incredibly time-consuming; if your Verilog outputs bad data, you must be able to definitively rule out a mathematical error. This Python model will serve as the exact blueprint your FPGA must replicate.

---

## Work Block 1: Mastering Fixed-Point Formatting (2 Hours)
FPGAs lack native floating-point processing units. To perform math on the Tang Nano, you will map floating-point values into 16-bit integers using **Q1.15 format** (1 sign bit, 15 fractional bits).

* **The Math:** * Float to Q1.15: Multiply by $2^{15}$ (32,768) and round to the nearest integer.
  * Q1.15 to Float: Divide by $2^{15}$.
* **Execution:**
  1. Set up a new Python virtual environment and install `numpy`, `scipy`, and `matplotlib`.
  2. Write a utility file (`q_math.py`) with two functions: `float_to_q115()` and `q115_to_float()`.
  3. Implement strict bounding: Since a 16-bit signed integer has a range of -32,768 to 32,767, your `float_to_q115()` function must explicitly catch and saturate (cap) any values that exceed this range to mimic hardware overflow protection.

## Work Block 2: Generating FIR Coefficients (2 Hours)
You need to design the actual Low-Pass Filter (LPF) that will strip out the high-frequency noise from your synthetic signal.

* **Execution:**
  1. Create a script named `generate_coeffs.py`.
  2. Use `scipy.signal.firwin` to generate a 15-tap low-pass filter. 
     * *Parameters to test:* A sample rate of 25 MHz (matches the FPGA clock) and a cutoff frequency of around 1 MHz.
  3. Pass the resulting floating-point array through your `float_to_q115()` function.
  4. Write a function to export these 15 integers into a text file named `fir_coeffs.hex`. Format the output as zero-padded hexadecimal strings (e.g., `0x1A4F`), placing one value per line. 

## Work Block 3: The Golden Model Convolution (4 Hours)
This is the core simulation. You must model the discrete-time FIR equation exactly as the hardware will execute it, including bit-truncation at every stage.
$$y[n] = \sum_{k=0}^{N-1} h[k] \cdot x[n-k]$$

* **Execution:**
  1. Create `golden_model.py`.
  2. **Generate the Stimulus:** Create an array simulating a clean 100 kHz sine wave. Create a second array simulating 5 MHz high-frequency noise. Add them together to create your `noisy_input` array. Scale the amplitude so it fits cleanly within your Q1.15 bounds.
  3. **The Hardware-Accurate Loop:** Do not use `numpy.convolve`. Write a custom `for` loop that iterates through the `noisy_input` array. 
  4. For each sample, multiply it by the coefficients. 
  5. *Crucial Step:* In hardware, multiplying two 16-bit numbers yields a 32-bit number. To pass this result to the next stage, you must right-shift it by 15 bits (`>> 15`) to bring it back to Q1.15 format. Your Python loop must explicitly perform this bit-shift and truncation to perfectly match the FPGA's behavior.

## Work Block 4: Visualization & Testbench Export (2 Hours)
You need to visually verify that your math successfully filters the wave, and then package the data so your Verilog tools can use it next week.

* **Execution:**
  1. Use `matplotlib.pyplot` to plot three subplots: the clean wave, the noisy input wave, and your filtered output wave. If the filtered wave resembles the clean wave, your Q1.15 math is correct.
  2. Export the `noisy_input` array to a file named `stimulus.hex` (one hex value per line).
  3. Export your filtered output array to a file named `expected_output.hex` (one hex value per line).

---

## Week 1 Deliverables Checklist
Before starting Week 2, ensure these files are committed to your repository:
* [ ] `q_math.py` (Fixed-point conversion utilities)
* [ ] `fir_coeffs.hex` (15 lines of hex data for the filter taps)
* [ ] `stimulus.hex` (The raw, noisy data to feed the Verilog testbench)
* [ ] `expected_output.hex` (The baseline data to compare against the Verilog output)
* [ ] A saved `.png` chart proving the filter successfully removes noise in Python.