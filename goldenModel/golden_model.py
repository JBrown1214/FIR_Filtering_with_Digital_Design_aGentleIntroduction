from goldenModel.q115_conversions import float_to_q115, q115_to_float
from generate_coeffs import hexify_float_array
import numpy as np
from scipy.signal import kaiserord, lfilter, firwin, freqz
from pylab import figure, clf, plot, xlabel, ylabel, xlim, ylim, title, grid, axes, show, ion



# Constants
freq_base = 100e3                 # wave frequency [Hz]
fs = 25e6                         # sampling rate [Hz]
duration = 50e-6                  # duration, [sec]
amplitude = .5                   # base_wave amplitude [+float]
Ns = int(fs * duration)           # total number of samples, [+int]
t = np.arange(Ns) / fs            # timesteps [array[float]]

# 15 tap FIR filter coefficients
fc = 1e6        # cutoff frequency (Hz)
taps = 15       # number of taps (int)
fir_coeff = firwin(taps, cutoff = fc, fs = fs)


def mess_up_wave(base_wave):

    # noising_wave = np.sin(np.pi*2*t*freq_noise)
    
    true_noise = np.random.uniform(low=(-1.0 + amplitude), high= (1-(2**-15)-amplitude), size=Ns)

    messy_wave = base_wave + true_noise


    plot_waves(base_wave, true_noise, messy_wave)

    return messy_wave


def FIR_filter(messy_signal):
    clean_signal = []
    # for each y[n] (1-len(messy_signal)):
        # for each tap (1-15)
            # sum tap * x[n]
    
    for n in range(len(messy_signal)):
        y_n = 0.0
        for tap in range(len(fir_coeff)):
            if n-tap >= 0:
                y_n += fir_coeff[tap] * messy_signal[n-tap]
        clean_signal.append(y_n)
    
    plot_waves(clean_signal)

    return clean_signal


def plot_waves(*waves):
    ion()
    for i in range(len(waves)):
        figure()
        plot(t, waves[i], linewidth=1)
        xlim(0, duration)
        ylim(-2.15, 2.15)
        grid(True)

    show()


def main():
    base_wave = np.sin(np.pi*2*t*freq_base) * amplitude 
    messy_signal = mess_up_wave(base_wave)
    clean_signal = FIR_filter(messy_signal)

    hexify_float_array(messy_signal, "messy_stimulus")
    hexify_float_array(base_wave, "expected_output")

    show(block=True)
    
    return clean_signal

if __name__ == "__main__":
    main()