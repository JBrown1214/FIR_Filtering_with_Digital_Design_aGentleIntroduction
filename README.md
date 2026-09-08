# FIR Filter RTL Implementation

*September 2026 Update*

Welcome to my digital design project! This repository contains my work on building a 47-tap Finite Impulse Response (FIR) filter in SystemVerilog. 

I chose this project as a self-guided introduction to verilog as a beginner at digital design. I learned a little Verilog in ECE 352 (intro to digital design), and brushed up my Verilog in the early summer of 2026 with HDLbits.com. This project was inspired greatly by ECE 352 and ECE 203 (intro to signal processing). This semester (Fall 2026) I am taking ECE 551, which is more Verilog intensive, and this project was great self-study to prepare myself. 

Note on AI: I'm building this project from the ground up to demonstrate my understanding of DSP concepts, hardware architecture, and modern functional verification methodologies. AI is not being used for Verilog code generation, and is being used sparingly for python code/housekeeping. As this is one of my first Verilog projects, I would rather push shoddy, beginner Verilog code that I wrote than a massive repo of AI slop. I hope that a scan through my commit history, comments, and code, will demonstrate the intention I have put into the learning process of this project. 

## Project Status

Currently, the **SystemVerilog RTL** is complete, and the **Golden Model (Python)** is in active development after inconsistencies were found in the golden model rounding. 

### What's Done
*   **RTL Architecture Design**: 
    *   Scaled the architecture from an initial 15-tap parallel filter to a more complex 47-tap FIR filter.
    *   Designed and refactored the data path into a 9-stage pipelined tree structure to optimize timing (see schematics and diagrams in repo).
    *   Completed the SystemVerilog implementation (`fir_filter_top.sv`).
*   **Verification Stack Setup (`/RTL_Architecture`)**: 
    *   Configured a modern, open-source verification flow using **Verilator**, **cocotb**, and **Surfer**.
    *   Python-based testbenches (`pytest` for the golden model, `cocotb` for the RTL) are up and running.

### What I'm Working On Next
*   **Fixing Golden Model Rounding Issues**: 
    *   I discovered a 1-bit hex rounding error inconsistency in the Python reference model.
    *   I am currently tracking down this discrepancy, which is likely within the floating-point to Q1.15 fixed-point format conversions.
*   Once the golden model rounding is fixed, I will re-run the full `cocotb` verification suite to ensure perfect bit-accurate matching between the model and the SystemVerilog RTL.

## Repository Structure
*   `goldenModel/`: Python reference model, Q1.15 fixed-point conversion scripts, and test vector generation. (in progress...)
*   `RTL_Architecture/`: SystemVerilog source files (`.sv`), cocotb testbenches, and the Makefile for simulation.
*   `FIRf diagram 1/2`: Architecture plans and visual diagrams (e.g., pipelining strategies).
*   `tests/`: `pytest` suite for the Python golden model and Q1.15 math logic. (in progress...)

## Tech Stack
*   **Hardware Description**: SystemVerilog
*   **Modeling & Scripting**: Python, NumPy, SciPy
*   **Verification**: cocotb, Verilator, pytest
*   **Waveform Viewer**: Surfer

---
*Feel free to poke around the commit history to see how the architecture has evolved. I am actively pushing updates as I build out the RTL!*
