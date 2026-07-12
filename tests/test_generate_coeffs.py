from goldenModel.generate_coeffs import output_float_array_file, fir_coeff
from config import *

def test_output_float_array_file():
    fir_coeff_hex = output_float_array_file(fir_coeff)
    
    for i in range(len(fir_coeff_hex)//2):
        assert fir_coeff_hex[i] == fir_coeff_hex[-(i+1)]
