import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
import numpy as np
from scipy.signal import firwin
from pylab import figure, plot, xlabel, ylabel, xlim, ylim, title, grid, axes, show, ion
from config import *
from goldenModel.qFormat_conversions import float_to_qFormat, qFormat_to_float
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

    for n in range(len(messy_signal)):
        y_accum = 0
        for tap in range(len(fir_coeff)):
            if n-tap >= 0:
                y_accum += (fir_coeff[tap] * messy_signal[n-tap])
        # lossy conversion to ensure python golden model values match FPGA
        clean_signal.append(qFormat_to_float(float_to_qFormat(y_accum,7,15),7,15)) #? Q-format fixed?
    
    # Note: I likely will have to add padding here to account for the pipeline loading 
    # at the start of my verilog function (prepend with some zeros)
    
    plot_waves(clean_signal)

    return clean_signal


def plot_waves(*waves):
    ion()
    for i in range(len(waves)):
        figure()
        plot(t, waves[i], linewidth=.75)
        xlim(0, DURATION)
        ylim(-2.15, 2.15)
        grid(True)

    show()


def main():
    base_wave = np.sin(np.pi*2*t*FREQ_BASE) * BASE_WAVE_AMPLITUDE 
    print(f"Your signal to noise ratio (db) is: {20 * np.log(BASE_WAVE_AMPLITUDE/(1-BASE_WAVE_AMPLITUDE))}")
    messy_signal = mess_up_wave(base_wave)
    clean_signal = FIR_filter(messy_signal) #? Q-format fixed?

    #! Potential Q-probs in output_float_array_file()
     #? Q-format fixed? (technically fine becase this func is never called with -1<vals<1)
    output_float_array_file(messy_signal, "messy_stimulus") #?
    output_float_array_file(clean_signal, "expected_output") #?

    output_float_array_file(fir_coeff, "fir_coeffs", "HEX") #?
    output_float_array_file(fir_coeff, "fir_coeffs", "DEC")

    show(block=True)
    
    return clean_signal

if __name__ == "__main__":
    main()