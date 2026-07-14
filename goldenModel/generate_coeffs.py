# https://scipy-cookbook.readthedocs.io/items/FIRFilter.html
# https://en.wikipedia.org/wiki/Finite_impulse_response
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.firwin.html

from scipy.signal import firwin
from goldenModel.q115_conversions import float_to_q115
from config import *


# FIR filter coefficients
fir_coeff = firwin(TAPS, cutoff = FC, fs = FS)

def output_float_array_file(float_array_in, array_name="default_arrayname", output_type="HEX"):
    if array_name != "default_arrayname":
        if output_type == 'HEX':
            q115_array = []
            for i in float_array_in:
                q115 = float_to_q115(i)
                # "Smoke test" catch
                # TODO: throw an error here, not just print a warning
                if q115 > 0xFFFF:
                    print("====================")
                    print("-----ERROR: bad Q1.15 value!-----\n" \
                    f"Your Q1.15 value was {q115}, which is greater than 16 bits of binary :/ \n"
                    "that would've smoked your FPGA logic. " \
                    " You should check your Q1.15 conversions")
                    print("====================")
                q115_array.append(q115)
            with open(f"{array_name}.hex", "w") as output_file_hex:
                str_array = []
                for q115 in q115_array:
                    str_array.append(f"{q115:0x}")
                output_file_hex.write('\n'.join(str_array))
            return q115_array
        elif output_type == 'DEC' or 'DECIMAL':
            with open(f"{array_name}_decimal.txt", "w") as output_file_dec:
                str_array = []
                for f in float_array_in:
                    str_array.append(str(f))
                output_file_dec.write('\n'.join(str_array))
            return float_array_in
    else:
        str_array = []
        for i in float_array_in:
            q115 = (float_to_q115(i))
            if q115 > 0xFFFF:
                str_array.append(f"{q115:0x}")

    return str_array



def main():
    output_filename_1 = "fir_coeffs"

    fir_coeff_hex = output_float_array_file(fir_coeff, output_filename_1, "HEX")
    fir_coeff_dec = output_float_array_file(fir_coeff, output_filename_1, "DEC")
    
    # with open(f"{output_filename}.hex") as f:
    #     print(f.read())
    # print()
    # print(fir_coeff_hex)


    

if __name__ == "__main__":
    main()