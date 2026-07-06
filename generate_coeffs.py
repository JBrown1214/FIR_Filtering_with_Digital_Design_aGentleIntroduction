# https://scipy-cookbook.readthedocs.io/items/FIRFilter.html
# https://en.wikipedia.org/wiki/Finite_impulse_response
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.firwin.html

from scipy.signal import firwin
from q115_conversions import float_to_q115


def make_q115_fir_coeffs(fs, fc, taps):
    fir_coeff = firwin(taps, cutoff = fc, fs = fs)


    fir_coeff_q115 = []
    for i in fir_coeff:
        fir_coeff_q115.append(float_to_q115(i))

    return fir_coeff_q115


def main():
    fs = 25e6       # sampling frequency (Hz)
    fc = 1e6        # cutoff frequency (Hz)
    taps = 15       # number of taps (int)

    fir_coeff_q115 = make_q115_fir_coeffs(fs, fc, taps)

    with open("fir_coeffs.hex", "w") as output_file_hex:
        for coeff in fir_coeff_q115:
            if coeff > 32768:
                print("This would've smoked your FPGA logic. " \
                "   You should check your Q1.15 conversions")
            else:
                output_file_hex.write(f"0x{coeff:0x}\n")
    
    with open("fir_coeffs.hex") as f:
        print(f.read())

if __name__ == "__main__":
    main()