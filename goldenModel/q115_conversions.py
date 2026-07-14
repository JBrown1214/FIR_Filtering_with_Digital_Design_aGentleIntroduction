"""
q115_conversions.py 

This file stores methods for converting between float values and Q1.15 format binary values

For more on Q number formatting see: 
    https://onlinedocs.microchip.com/oxy/GUID-70ACD6B0-A33F-4653-B192-8465EAD1FD98-en-US-11/GUID-B8396BB4-C5C6-4E10-A0DC-C32A4B031857.html
    https://en.wikipedia.org/wiki/Q_(number_format)
 
We are using Q1.15, meaning there is one sign bit (+-) and 15 fraction bits 
Each fractional bit represents 2^-N, this means Q1.15 can represent -1.0 to +0.999969482 

q115 values are represented in the code as integers (which python stores as binary values)
    e.g. 
    q115 = 10 (integer 10) is stored as 4'b1010, which sign extends to 0x000A
    this q115 value is equivalent to the float value +0.00030517578 = (2**-14 + 2**-12)
"""
import math
import numpy as np
from config import *

# Q1.15 fixed-point constants
# Max positive float value is 1 - (2^-15), which is 0.99996948242
Q115_F_MAX_POS = 1.0 - (2**-15)
Q115_F_MAX_NEG = -1.0

Q115_HEX_MAX_POS = 0x7FFF
Q115_HEX_MAX_NEG = 0x8000
Q115_HEX_MAX_INT = 0xFFFF

def float_to_q115(float_in):
    """
    converts a float value to an integer value whose bits map to Q1.15 format
    Uses python bit masking to cut off values out of bounds (>0.999969... or <-1.0)

    Args:
        float_in: input float. Values greater than 1/-1 will be truncated to the nearest value
        (e.g. 1.5 will be stored as 1.0, -3 will be stored as -1)

    Returns:
        int: an int value representing the float in Q1.15 format. 
        (0-32767 for non-neg values, 32768-65535 for negative values)
    """

    # "Left shift" input to be Q115 format
    magn_q115 = abs(round(float_in * (2**15)))

    # Note: from this point onwards, Q1.15 values should always be a positive integer
    # negative Q1.15 values' will be > 32767, meaning that their binary will start with 'b1XX....XX

    if float_in > 0:
        if float_in > (1-(2**-15)):
            # float out of bounds: shorten to max Q1.15
            int_q115_masked = 0x7FFF
        else:
            int_q115_masked = ((magn_q115) & 0xFFFF)
    elif float_in < 0:
        if float_in < -1.0:
            # float out of bounds: shorten to max Q1.15
            int_q115_masked = 0x8000
        else:
            # we are fine to 2s comp before masking because we know the value is > -1.0 
            # flip 2s comp: negate and add 1
            int_q115 = (magn_q115 ^ 0xFFFF) + 1

            # bit mask to size
            int_q115_masked = int_q115 & 0xFFFF
    else: 
        int_q115_masked = (magn_q115 & 0xFFFF)
    

    return (int_q115_masked)


def q115_to_float(int_q115):
    """
    converts an integer representing a Q1.15 value into a float

    Args:
        int_q115: an int in Q1.15 format binary

    Returns:
        float: a float representation of the Q1.15 value. (-1.0 to +0.99996948242)

    Raises: 
        ____Error: if input value falls outside of the valid Q1.15 range [32767,-32768]
    """
    if int_q115 > 0xFFFF:
        # this should never happen
        # TODO: throw a warning here

        # we will just bitmask down to size then treat the first 16 bits as the new value 
        int_q115 = int_q115 & 0xFFFF
        if int_q115 >= 0x8000:
            return Q115_F_MAX_NEG
        else:
            return Q115_F_MAX_POS

    # float value is negative
    if int_q115 >= 0x8000: 
        # 2s comp flip: negate, add 1, then return float conversion
        return -((int_q115 ^ 0xFFFF)+1)/(2**15)
        
        # if int_q115 == 0x8000:
        #     return -1.0
        # return (-(int_q115 & 0x7FFF)/(2**15))

    # float value is positive
    else: 
        return (int_q115/(2**15))
    
    
    # if f"{int_q115:016b}"[0] == '1':
    #     if (int_q115 > 32767):
    #         int_q115 = (int_q115 ^ 0xFFFF) +1
    #     return (-(int_q115)/(2**15))
    
    # if (int_q115 > 32767):
    #     int_q115 = 32767

    # return (int_q115/(2**15))


def main():
    for i in range(21):
        j = i/20
        if (j == q115_to_float(float_to_q115(j))):
            print(f"=====Let's go: your code is working at least partially: {j} =====")
            print()
        else:
            print(f"    Here is your starting float:                        {j}")
            print(f"    Here is the binary that Q1.15 got turned into:      {float_to_q115(j):016b}")
            k = q115_to_float(float_to_q115(j))
            print(f"    Here is the float that Q1.15 got turned  into:      {k}")
            print(f"    The difference is                                   {j - k}")
            print()


if __name__ == "__main__":
    main()