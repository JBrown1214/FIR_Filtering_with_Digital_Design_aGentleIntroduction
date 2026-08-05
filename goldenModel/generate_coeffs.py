# https://scipy-cookbook.readthedocs.io/items/FIRFilter.html
# https://en.wikipedia.org/wiki/Finite_impulse_response
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.firwin.html

from scipy.signal import firwin
from goldenModel.qFormat_conversions import float_to_qFormat
from config import *
from pathlib import Path
SCRIPT_DIR = Path(__file__).resolve().parent


# FIR filter coefficients
fir_coeff = firwin(TAPS, cutoff = FC, fs = FS)

def output_float_array_file(float_array_in, array_name="default_arrayname", output_type="HEX"):
    if array_name != "default_arrayname":
        
        if output_type == 'HEX':
            # Target path: /FIR_RTL/goldenModel/{array_name}.hex
            file_path = SCRIPT_DIR / f"data_{array_name}.hex"
            
            qFormat_array = []
            for i in float_array_in:
                qFormat = float_to_qFormat(i) #? Q-format fixed? (technically fine becase this func is never called with -1<vals<1)
                if qFormat > 0xFFFF:
                    print("====================")
                    print("-----ERROR: bad qFormat value!-----\n" \
                    f"Your qFormat value was {qFormat}, which is greater than 16 bits of binary :/ \n"
                    "that would've smoked your FPGA logic. " \
                    " You should check your qFormat conversions")
                    print("====================")
                qFormat_array.append(qFormat)
                
            with open(file_path, "w") as output_file_hex:
                str_array = [f"{qFormat:04x}" for qFormat in qFormat_array]  # 04x ensures 4-digit hex padding
                output_file_hex.write('\n'.join(str_array))
            
            print(f"[+] Output written to: {file_path}")
            return qFormat_array

        elif output_type in ('DEC', 'DECIMAL'):
            # Target path: /FIR_RTL/goldenModel/{array_name}_decimal.txt
            file_path = SCRIPT_DIR / f"data_{array_name}_decimal.txt"
            
            with open(file_path, "w") as output_file_dec:
                str_array = [str(f) for f in float_array_in]
                output_file_dec.write('\n'.join(str_array))
                
            print(f"[+] Output written to: {file_path}")
            return float_array_in

    else:
        str_array = []
        for i in float_array_in:
            qFormat = float_to_qFormat(i)  #? Q-format fixed? (technically fine becase this func is never called with -1<vals<1)
            if qFormat > 0xFFFF:
                str_array.append(f"{qFormat:0x}")
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