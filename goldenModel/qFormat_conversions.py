"""
qFormat_conversions.py 

This file stores methods for converting between float values and qFormat format binary values

For more on Q number formatting see: 
    https://onlinedocs.microchip.com/oxy/GUID-70ACD6B0-A33F-4653-B192-8465EAD1FD98-en-US-11/GUID-B8396BB4-C5C6-4E10-A0DC-C32A4B031857.html
    https://en.wikipedia.org/wiki/Q_(number_format)
 
/*============ a note on notation ============
    I am using Q number formatting (see: https://en.wikipedia.org/wiki/Q_(number_format))
    More specifically: I am using ARM style Q number formating. 

    All Q number formats use "U" sign bits (-2^0), "m" integer bits (2^m), and "n" fractional bits (2^-n)
    To quote wikipedia: 
        """
"""     The Q notation... consists of the letter Q followed by a pair 
        of numbers m.n, where m is the number of bits used for the integer part of the value, 
        and n is the number of fraction bits.

        By default, the notation describes signed binary fixed point format, with the unscaled integer 
        being stored in two's complement format, used in most binary processors. As such, the first bit 
        always gives the sign of the value (1 = negative, 0 = non-negative), and it is not counted
        in the m parameter. Thus, the total number w of bits used is 1 + m + n.

        In particular, when n is zero, the numbers are just integers. If m is zero, all bits except the 
        sign bit are fraction bits; then the range of the stored number is from -1.0 (inclusive) to +1.0 (exclusive).
"""        """

    According to the ARM variant of Q notation, the sign bit and integer bit(s) are added together
        e.g. Q1.15 is 1 sign bit  + (0 integer bits) + 15 fractional bits (2^-1 through 2^-15).
============================================*/

qFormat values are represented in the code as integers (which python stores as binary values)
    e.g. 
    qFormat = 10 (integer 10) is stored as 4'b1010, which sign extends to 0x000A
    this qFormat value is equivalent to the float value +0.00030517578 = (2**-14 + 2**-12)
"""
import math
import numpy as np
from config import *

# Q1.15 constants
#     # Max positive float value is 1 - (2^-15), which is 0.99996948242
#     qFormat_F_MAX_POS = 1.0 - (2**-15)
#     qFormat_F_MAX_NEG = -1.0


#     qFormat_HEX_MAX_POS = 0x7FFF
#     qFormat_HEX_MAX_NEG = 0x8000
#     qFormat_HEX_MAX_INT = 0xFFFF

def float_to_qFormat(float_in, intbit = 0, fracbit = 15):
    """
    converts a float value to an integer value whose bits map to qFormat
    """

    if intbit < 0:
        print("cannot have negative number of integer bits in q-format")
    if fracbit < 0:
        print("cannot have negative number of fractional bits in q-format")


    Qformat_int = round(float_in * (2**fracbit))

    # "Left shift" input to be Q format
    magn_float_in = abs(Qformat_int)


    if float_in > 0:
        maxval_mask = (1 << (fracbit + intbit - 1)) - 1
    elif float_in < 0:
        maxval_mask = (1 << (fracbit + intbit - 1))
    else: 
        return 0
    
    if (magn_float_in > maxval_mask):
        if float_in < 0:
            mask_ones = (1 << (fracbit + intbit)) - 1
            return ((maxval_mask ^ mask_ones)+1) # 2s comp flip
        return maxval_mask
    else:
        if float_in < 0:
            mask_ones = (1 << (fracbit + intbit)) - 1
            return ((magn_float_in ^ mask_ones)+1) # 2s comp flip
        return (Qformat_int)


def qFormat_to_float(int_qFormat, intbit = 0, fracbit = 15):
    """
    converts an integer representing a qFormat value into a float
    """


    if intbit < 0:
        print("cannot have negative number of integer bits in q-format")
    if fracbit < 0:
        print("cannot have negative number of fractional bits in q-format")

    isNegative = (int_qFormat >> (fracbit + intbit - 1)) & 1

    if isNegative: 
        mask_ones = (1 << (fracbit + intbit)) - 1
        return -((int_qFormat ^ mask_ones)+1)/(2**fracbit) # 2s comp flip
    else: 
        return (int_qFormat/(2**fracbit))

def main():
    for i in range(21):
        j = i/20
        if (j == qFormat_to_float(float_to_qFormat(j))):
            print(f"=====Let's go: your code is working at least partially: {j} =====")
            print()
        else:
            print(f"    Here is your starting float:                        {j}")
            print(f"    Here is the binary that qFormat got turned into:      {float_to_qFormat(j):016b}")
            k = qFormat_to_float(float_to_qFormat(j))
            print(f"    Here is the float that qFormat got turned  into:      {k}")
            print(f"    The difference is                                   {j - k}")
            print()


if __name__ == "__main__":
    main()