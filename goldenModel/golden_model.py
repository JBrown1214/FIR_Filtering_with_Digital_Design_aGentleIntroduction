import sys
from datetime import datetime
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
import numpy as np
from scipy.signal import firwin
import matplotlib.pyplot as plt
from config import *
from goldenModel.qFormat_conversions import float_to_qFormat, qFormat_to_float, lossy_conversion
from goldenModel.generate_coeffs import output_float_array_file


# Constants
Ns = int(FS * DURATION)     # total number of samples, [+int]
t = np.arange(Ns) / FS      # timesteps [array[float]]

# FIR filter coefficients
fir_coeff = firwin(TAPS, cutoff = FC, fs = FS)


def mess_up_wave(base_wave):

    # noising_wave = np.sin(np.pi*2*t*freq_noise)
    
    true_noise = np.random.uniform(low=(-1.0 + BASE_WAVE_AMPLITUDE), high= (1-(2**-15)-BASE_WAVE_AMPLITUDE), size=Ns)

    messy_wave = base_wave + true_noise


    plot_waves(base_wave, true_noise, messy_wave)

    return messy_wave


def FIR_filter(messy_signal):
    clean_signal = []
    
    # Calculate true middle index (23 for a 47-tap filter)
    mid_tap = len(fir_coeff) // 2
    num_taps = len(fir_coeff)

    for n in range(len(messy_signal)):

        y_accum = 0
        for tap in range(mid_tap):    # loops 0-22 (excludes 23)
            
            # Causal pre-adder matching x_reg[i] + x_reg[46-i]
            # Values prior to time 0 are 0 (simulates RTL reset state)
            x_tap = messy_signal[n - tap] if (n - tap) >= 0 else 0.0
            x_mirror = messy_signal[n - (num_taps - 1 - tap)] if (n - (num_taps - 1 - tap)) >= 0 else 0.0
            
            coeff = lossy_conversion(fir_coeff[tap])

            # pre-add and multiply stages 
            tapval = coeff * (lossy_conversion(x_tap) + lossy_conversion(x_mirror))
            
            # Allow bit growth (no intermediate quantization)
            y_accum += tapval

        # Separately add the middle tap
        x_mid = messy_signal[n - mid_tap] if (n - mid_tap) >= 0 else 0.0
        coeff = lossy_conversion(fir_coeff[mid_tap])      
        y_accum += lossy_conversion(x_mid) * coeff


        # round to Q1.15 at the very end of summation (matches RTL right-shift stage)
        clean_signal.append(lossy_conversion(y_accum,1,15)) #? Q-format fixed?

    plot_waves(clean_signal, seed="GoldenOUT_")

    return clean_signal


def plot_waves(*waves, seed="", overlay=False, dynamic_ylims=False):
    output_dir = Path("output_plots")
    output_dir.mkdir(parents=True, exist_ok=True)

    # setup plot for overlap or not
    if overlay:
        figures = [
            (list(enumerate(waves)), "Overlaid Waves", f"{seed}waves_overlay.png")
        ]
    else:
        figures = [
            ([(i, wave)], f"Wave {i + 1}", f"{seed}wave_{i + 1}.png")
            for i, wave in enumerate(waves)
        ]

    # Plot everything
    for wave_group, title, filename in figures:
        fig, ax = plt.subplots()

        for idx, wave in wave_group:
            ax.plot(range(len(wave)), wave, linewidth=0.75, label=f"Wave {idx + 1}")

        if dynamic_ylims:
            ax.autoscale(axis="x")
            ax.margins(y=0.10)
        else:
            ax.set_ylim(-2.15, 2.15)
        ax.grid(True)
        ax.set_title(title)
        if overlay:
            ax.legend(loc="upper right")

        filepath = output_dir / filename
        fig.savefig(filepath, bbox_inches="tight", dpi=300)
        print(f"Saved: {filepath}")

        plt.close(fig)

    return output_dir


def plot_delta_histogram(delta_count, filename="delta_histogram.png"):
    # Sort keys numerically so the chart reads logically left-to-right
    sorted_pairs = sorted(delta_count.items(), key=lambda item: int(item[0]))

    # Convert keys to str for equal bar widths
    x_categories = [str(k) for k, v in sorted_pairs]
    y_counts = [v for k, v in sorted_pairs]

    fig, ax = plt.subplots()
    ax.bar(x_categories, y_counts, color="royalblue", edgecolor="black")

    max_y = max(y_counts) if y_counts else 1
    ax.set_ylim(0, max_y * 1.15)

    ax.set_title("Error Delta Distribution")
    ax.set_xlabel("Delta Value")
    ax.set_ylabel("Occurrences")
    ax.grid(axis="y", linestyle="--", alpha=0.7)

    output_path = Path("output_plots") / filename
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fig.savefig(output_path, bbox_inches="tight", dpi=300)
    plt.close(fig)  # Free memory
    print(f"Saved histogram to: {output_path}")


def main():
    base_wave = np.sin(np.pi*2*t*FREQ_BASE) * BASE_WAVE_AMPLITUDE 
    print(f"Your signal to noise ratio (db) is: {20 * np.log(BASE_WAVE_AMPLITUDE/(1-BASE_WAVE_AMPLITUDE))}")
    messy_signal = mess_up_wave(base_wave)
    clean_signal = FIR_filter(messy_signal) #? Q-format fixed?

    #? Q-format fixed? (technically fine becase this func is never called with -1<vals<1)
    output_float_array_file(messy_signal, "messy_stimulus") #?
    output_float_array_file(clean_signal, "expected_output") #?

    output_float_array_file(fir_coeff, "fir_coeffs", "HEX") #?
    output_float_array_file(fir_coeff, "fir_coeffs", "DEC")

    return clean_signal

if __name__ == "__main__":
    main()