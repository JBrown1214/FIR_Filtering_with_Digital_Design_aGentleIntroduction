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

# Python doesn't like integers starting with 0, so Q1.15 values will be formatted as strings

# takes a float (python value) and map it to a Q1.15 bit-interpretation
    # input: float (base 10)
    # step 1: multiply by 2**15 (effectively L shift by 15 decimal points)
    #           We now have an int value, which shoudl be between 32767 and -32768. 
    # step 10: Repeatedly mod2 to find bits; store in array
    #           output_binary = IntValue % 2 # output will be 1/0
    # step 11:  check original input: negative? 2's Comp flip the values (very annoying)
def float_to_q115(INfloat):
    
    # step 1: Left shift input, filter to cap values exceeding range
    Lshift_IN = round(INfloat * 2**15)
    # filter to fit range
    if (Lshift_IN > 32767):
        Lshift_IN = 32767
    elif (Lshift_IN < -32768):
        Lshift_IN = -32768

    # print(f"{(Lshift_IN):016b}")

    # step 10: store int value in an array as 16 bits of signed binary
    # Values are stored here in big-endian format
    q115_Arr = []  
    while abs(Lshift_IN) >= 1:
        q115_Arr.append(int(Lshift_IN % 2))
        Lshift_IN = int(Lshift_IN / 2)
    if (len(q115_Arr) < 16):            # extend to 16 bits, if needed
        bits_to_extend = 16 - len(q115_Arr)
        for i in range(bits_to_extend):
            q115_Arr.append(0)          # always extend zero (2sComp later if needed)
    
    # step 11: convert value to two's comp negative, if value is negative
    # (positive values will inherently be in the correct format)
    if INfloat < 0:
        Flip_TwosComp(q115_Arr)
    

    # convert from list to string, flip back to little-Endian in the process
    OUTq115 = ""
    for i in range(len(q115_Arr)):
        OUTq115 += str(q115_Arr.pop())
    
    return (OUTq115)



def q115_to_float(INq115):
    str_INq115 = str(INq115)
    magnVal = 0.0
    for i in range(1,16,1):
        if int(str_INq115[i]):
            magnVal += 2**(-i)
    if str_INq115[0] == '1':
        magnVal -= 1.0
    return magnVal


# Big Endian Notation input!!!
def Flip_TwosComp(InArr):
    TwosCompArr = []
    
    # Negate
    for i in range(len(InArr)):
        TwosCompArr.insert(i, (1 - InArr[i])) # 1-1 is 0, 1-0 is 1; flips all values
    
    # Add one (to least significant digit)
    for i in range(len(TwosCompArr)):
        if TwosCompArr[i] == 0:     # find first non-1 value 
            TwosCompArr[i] = 1      # flip it to 1 (simplified addition-carry)
            InArr = TwosCompArr     # ensure method is in-place
            return InArr            # (I could remove this line if I really wanted...)
    # if all values of negated array are 1, input array was all zeros; return input array
    return InArr


# QUICK TESTS
for i in range(21):
    j = i/20
    if (j == q115_to_float(float_to_q115(j))):
        print(f"=====Let's go: your code is working at least partially: {j} =====")
        print()
    else:
        print(f"    Here is your starting float:                        {j}")
        print(f"    Here is the binary that Q1.15 got turned into:      {float_to_q115(j)}")
        k = q115_to_float(float_to_q115(j))
        print(f"    Here is the float that Q1.15 got turned  into:      {k}")
        print(f"    The difference is                                   {j - k}")
        print()
