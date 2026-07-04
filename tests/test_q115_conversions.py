from q115_conversions import Flip_TwosComp, q115_to_float, float_to_q115

# Three tests to validate Q115 conversion behavior

def test_Flip_TwosComp():
    # These are Big-Endian
    testArray1 = [1,0,0,0] # +1 (should flip to binary -1 == 0xF)
    testArray2 = [1,1,1,0] # +7 (should flip to binary -7 == 0x9)
    testArray3 = [0,0,0,0] # should return 0x0
    testArray4 = [1,1,1,1] # -1 (should return +1 == 0x1)


    result1 = Flip_TwosComp(testArray1)
    result2 = Flip_TwosComp(testArray2)
    result3 = Flip_TwosComp(testArray3)
    result4 = Flip_TwosComp(testArray4)



    assert result1 == [1,1,1,1]
    assert result2 == [1,0,0,1]
    assert result3 == [0,0,0,0]
    assert result4 == [1,0,0,0]


def test_q115_to_float():
    Q115_1 = '0111111111111111' # 0x7FFF (.99...)
    Q115_2 = '1000000000000000' # 0x8000 (-1.0)
    Q115_3 = '0100000000000000' # 0x4000 (.5)
    Q115_4 = '1100000000000000' # 0xC000 (-0.5)

    result1 = q115_to_float(Q115_1)
    result2 = q115_to_float(Q115_2)
    result3 = q115_to_float(Q115_3)
    result4 = q115_to_float(Q115_4)

    assert result1 == 0.999969482421875
    assert result2 == -1.0
    assert result3 == 0.5
    assert result4 == -0.5


def test_float_to_q115():
    testFloat1 = 0.999969482
    testFloat2 = -1.0
    testFloat3 = .5
    testFloat4 = -0.5
    
    result1 = float_to_q115(testFloat1)
    result2 = float_to_q115(testFloat2)
    result3 = float_to_q115(testFloat3)
    result4 = float_to_q115(testFloat4)

    assert result1 == '0111111111111111'
    assert result2 =='1000000000000000'
    assert result3 == '0100000000000000'
    assert result4 == '1100000000000000'
