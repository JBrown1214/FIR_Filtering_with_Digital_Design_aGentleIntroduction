"""Configuration constants"""

# Wave constants
FS = 25e6                    # Sampling rate (frequency) [Hz]
FREQ_BASE = 100e3            # Wave frequency [Hz]
BASE_WAVE_AMPLITUDE = 0.4    # Base wave amplitude [float, 0.0 to 1.0]
DURATION = 50e-6                  # duration, [sec]

# FIR filter constants
FC = 1e6                     # Filter cutoff frequency [Hz]
TAPS = 47                    # Number of taps (must be odd for Type I/II FIR)



# Controlling wildcard imports (from config import *)
__all__ = [
    "FS",
    "FREQ_BASE",
    "BASE_WAVE_AMPLITUDE",
    "DURATION",
    "FC",
    "TAPS",
]