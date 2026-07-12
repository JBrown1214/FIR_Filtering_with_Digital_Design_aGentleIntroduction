# https://scipy-cookbook.readthedocs.io/items/FIRFilter.html
# https://en.wikipedia.org/wiki/Finite_impulse_response
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.firwin.html

from scipy.signal import firwin
from goldenModel.q115_conversions import float_to_q115

# Constants
fs = 25e6       # sampling frequency (Hz)
fc = 1e6        # cutoff frequency (Hz)
taps = 15       # number of taps (int)
fir_coeff = firwin(taps, cutoff = fc, fs = fs)


def hexify_float_array(float_array_in, array_name="input_array"):
    q115_array = []
    for i in float_array_in:
        q115_array.append(float_to_q115(i))

    with open(f"{array_name}.hex", "w") as output_file_hex:
        hex_str_array = []
        for q115 in q115_array:
            # "Smoke test" catch
            if q115 > 0xFFFF:
                print("====================")
                print("-----ERROR: bad Q1.15 value!-----\n" \
                f"Your Q1.15 value was {q115}, which is greater than 16 bits of binary :/ \n"
                "that would've smoked your FPGA logic. " \
                " You should check your Q1.15 conversions")
                print("====================")
            else:
                hex_str_array.append(f"{q115:0x}")
        output_file_hex.write('\n'.join(hex_str_array))
    return hex_str_array


def main():
    hexify_float_array(fir_coeff, "fir_coeffs")
    
    # with open("fir_coeffs.hex") as f:
    #     print(f.read())
    # print()
    # print(fir_coeff_q115)


    

if __name__ == "__main__":
    main()