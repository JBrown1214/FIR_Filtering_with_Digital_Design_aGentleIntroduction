# Project Plan: FPGA-Accelerated Dynamic FIR Filter

## 1. Context & Objective
* **Target:** Secure a lower-level embedded systems internship (Defense, Aerospace, MedTech, Big Tech) for Summer 2027.
* **Hardware:** ESP32 Microcontroller, Tang Nano 20K FPGA, basic electronics kit.
* **Constraints:** 6.5 weeks to achieve a 95% working project; strictly budgeted at ~10-12 hours/week (70-75 hours total).
* **Design Philosophy:** Exploit true FPGA capabilities (absolute determinism, nanosecond-level timing, parallel processing, custom hardware data paths). The FPGA must not be a glorified microcontroller wrapper; it must perform high-speed DSP tasks that would bottleneck the ESP32.

---

## 2. System Architecture & Interview Highlights

To elevate this from a standard class assignment to an internship-winning "headliner," the design avoids static, hardcoded logic and slow clocks. Instead, it demonstrates true hardware-software co-design through three key features:

### A. The Dynamic Register File (ESP32 Interface)
* **The Concept:** Filter coefficients are not hardcoded into Verilog logic. Instead, they are mapped to an internal Register File on the FPGA. 
* **The Execution:** The ESP32 sends configuration packets over SPI. The FPGA decodes these packets and writes new 16-bit fixed-point coefficients into its internal registers.
* **The "Why":** Proves an understanding of real SoC architectures. You are designing a dynamic hardware accelerator controlled by a host processor.

### B. High-Speed Synthetic Data Generation
* **The Concept:** Because standard starter kits lack high-speed ADCs, the high-speed data stream is simulated internally on the FPGA.
* **The Execution:** A "Signal Generator" module uses Direct Digital Synthesis (DDS) to generate a clean sine wave, injected with high-frequency digital noise via a Linear Feedback Shift Register (LFSR). 
* **The "Why":** Streams noisy synthetic signals into the FIR filter at the Tang Nano's native clock speed (25 MHz+), proving the hardware datapath operates at speeds an ESP32 cannot physically achieve in software.

### C. The "Zero-Overhead" Dual-Buffer Readout
* **The Concept:** The ESP32 needs to visualize the data without being interrupted for every single sample, which would choke the CPU.
* **The Execution:** A Dual-Port Block RAM (BRAM) inside the Tang Nano stores continuous "Raw" and "Filtered" streams. When the buffer fills, the FPGA drops an interrupt pin. The ESP32 pulls the data frame via SPI at its own pace and plots it on a web dashboard.
* **The "Why":** Demonstrates mastery of clock domain crossing, buffering, and efficient peripheral-to-CPU interrupt handling.

---

## 3. The 6.5-Week Execution Schedule (75 Hours)

### Week 1: Fixed-Point Math & Golden Model (10 Hours)
* **Goal:** Establish the mathematical foundation and verification baseline.
* **Tasks:**
  * Learn fixed-point number formatting (e.g., Q1.15 format).
  * Write a Python script to generate filter coefficients.
  * Develop the mathematical "golden model" in Python to process a noisy wave and output the clean wave. This will be used to verify the Verilog output later.

### Week 2: The Core FIR Architecture (12 Hours)
* **Goal:** Build and verify the digital signal processing pipeline.
* **Tasks:**
  * Write the Verilog for the shift registers, hardware multipliers, and pipelined adder tree.
  * Write a comprehensive ModelSim/Gowin testbench.
  * Feed the testbench a step function and compare the output against the Python Golden Model to prove the math works in simulation.

### Week 3: Synthetic Noise Engine & BRAM (10 Hours)
* **Goal:** Create the high-speed data source and the data-storage sink.
* **Tasks:**
  * Implement the LFSR noise injector and the internal DDS signal generator.
  * Wire the generator to the FIR filter input.
  * Instantiate the Gowin Block RAM (BRAM) to capture and store snapshots of both raw and filtered data.

### Week 4: SPI & Register Mapping (12 Hours)
* **Goal:** Build the hardware interface for the microcontroller.
* **Tasks:**
  * Design the SPI slave module on the Tang Nano.
  * Create the control registers. Ensure that writing an SPI byte successfully updates the active filter coefficients in the FIR pipeline.
  * Verify SPI timing and transactions in a testbench.

### Week 5: ESP32 Integration (12 Hours)
* **Goal:** Bridge the hardware and the software.
* **Tasks:**
  * Write the ESP32 C code (using ESP-IDF or FreeRTOS) to handle master SPI communication.
  * Write the firmware to calculate/select coefficients on the fly based on desired filter characteristics.
  * Implement the Interrupt Service Routine (ISR) to read back the BRAM signal snapshots when the FPGA signals data is ready.

### Week 6: The Web Visualizer & Polish (10 Hours)
* **Goal:** Create the visual "wow" factor for recruiters and interviewers.
* **Tasks:**
  * Set up a lightweight WebSockets or basic HTTP server on the ESP32.
  * Serve a simple web dashboard (using Chart.js or similar) that dynamically plots the raw vs. filtered waveforms.
  * Stress-test the system and fix any SPI data-corruption bugs.

### Week 6.5: Clean the Repository (4 Hours)
* **Goal:** Package the project for maximum visibility.
* **Tasks:**
  * Clean up and comment Verilog timing paths and C code.
  * Write a highly detailed GitHub README. Include architectural block diagrams, simulation waveforms (screenshots from ModelSim), and a GIF of the working web dashboard. 
  * Explicitly state in the README *why* an FPGA was used over a software-only approach.