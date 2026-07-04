import math
import numpy as np

# This relies on Q number formatting
# See: https://onlinedocs.microchip.com/oxy/GUID-70ACD6B0-A33F-4653-B192-8465EAD1FD98-en-US-11/GUID-B8396BB4-C5C6-4E10-A0DC-C32A4B031857.html
# See also: https://en.wikipedia.org/wiki/Q_(number_format)
# 
# We are using Q1.15, meaning there is one sign bit (+-)
# and 15 fraction bits (2^-1 (.5) --> 2^-15 (0.000030518)), (like sig figs)
# This means we can represent -1.0 up to +0.999969482 
# These functions convert between Q1.15 "decimal" to a float value

# takes a float (python value) an map it to a bit-interpretation
def float_to_q115(INfloat):
    return np.int16(INfloat * 2**15) 


def q115_to_float(INq115):

    return



def intB10_to_16b_2comp_Binary(INint):
    OUTbinary = ""
    while (abs(INint) > 1):
        if (INint % 2 == 1):
            if (INint > 0):
                OUTbinary = "1" + OUTbinary
            else: 
                OUTbinary = "0" + OUTbinary
        INint = math.floor(INint/2)
    if (abs(INint) == 1):
        OUTbinary = "1" + OUTbinary
    else:
        OUTbinary = "0" + OUTbinary
    
    if (len(str(OUTbinary)) < 16):
        OUTbinary = ("0" * (15 - len(str(OUTbinary)))) +OUTbinary
        if INint < 0:
            OUTbinary = "1" + OUTbinary
        else:
            OUTbinary = "0" + OUTbinary
    return OUTbinary




#TESTING



for i in range(10):
    for j in range(3):
        print(intB10_to_16b_2comp_Binary(i)[j:j+4] + "_", end="")
    print(intB10_to_16b_2comp_Binary(i)[-4:])
print("~~~~~~~~~~~")
print("sharpest tool in the shed.....")
for i in range(-10, 9, 1):
    for j in range(3):
        print(str(float_to_q115(i/10))[j:j+4] + "_", end="")
    print(str(float_to_q115(i/10))[-4:])

print()
print("=============Max positive value (0.999969...)=============")
print(intB10_to_16b_2comp_Binary(32767))
print("=============Max negative value (-1.0)=============")
print(intB10_to_16b_2comp_Binary(-32768))

print("--overflow values--")
for i in range(0,-10,-1):
    print(f"=====Int value is: {i - 32764}=====")
    for j in range(3):
        print(intB10_to_16b_2comp_Binary(i-32764)[j:j+4] + "_", end="")
    print(intB10_to_16b_2comp_Binary(i-32764)[-4:])


for i in range(10):
    print(np.binary_repr(np.int16(i)))