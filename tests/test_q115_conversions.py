from q115_conversions import q115_to_float, float_to_q115

# Three tests to validate Q115 conversion behavior


def test_q115_to_float():
    q115_1 = 0b0111111111111111     # 0x7FFF (.99...)
    q115_2 = 0b1000000000000000     # 0x8000 (-1.0)
    q115_3 = 0b0100000000000000     # 0x4000 (.5)
    q115_4 = 0b1100000000000000     # 0xC000 (-0.5)
    # TODO:  I could test cases where my Q1.15 is formatted wrong (too large/small)
    # q115_5 = 0b11000000000000000    # 0x18000 (should truncate extra bit and match -1.0)
    # q115_6 = 0b10111111111111111    # 0x17FFF (should truncate extra bit and match .99)

    result1 = q115_to_float(q115_1)
    result2 = q115_to_float(q115_2)
    result3 = q115_to_float(q115_3)
    result4 = q115_to_float(q115_4)
    # result5 = q115_to_float(q115_5)
    # result6 = q115_to_float(q115_6)

    assert result1 == 0.999969482421875
    assert result2 == -1.0
    assert result3 == 0.5
    assert result4 == -0.5
    # assert result5 == -1.0
    # assert result6 == 0.999969482421875


def test_float_to_q115():
    test_float_1 = 0.999969482
    test_float_2 = -1.0
    test_float_3 = .5
    test_float_4 = -0.5
    test_float_5 = 1.5      # (should shorten to .0.999969482)
    test_float_6 = -3       # (should shorten to -1.0)
    
    result1 = float_to_q115(test_float_1)
    result2 = float_to_q115(test_float_2)
    result3 = float_to_q115(test_float_3)
    result4 = float_to_q115(test_float_4)
    result5 = float_to_q115(test_float_5)
    result6 = float_to_q115(test_float_6)

    assert result1 == 0b0111111111111111
    assert result2 ==0b1000000000000000
    assert result3 == 0b0100000000000000
    assert result4 == 0b1100000000000000
    assert result5 == 0b0111111111111111
    assert result6 == 0b1000000000000000

