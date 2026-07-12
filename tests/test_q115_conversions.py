from goldenModel.q115_conversions import q115_to_float, float_to_q115
import pytest 
from goldenModel.q115_conversions import *


@pytest.mark.parametrize(
    ( "q115_input", "expected_float"), [
        (0b0111111111111111, Q115_F_MAX_POS),   # 0x7FFF
        (0b1000000000000000, Q115_F_MAX_NEG),   # 0x8000
        (0b0100000000000000,  0.5),             # 0x4000
        (0b1100000000000000, -0.5),             # 0xC000
        (0b0000000000000000, 0),                # 0x0000

        # below values are out of bounds, shorten to max Q1.15 regardless of value
            # sign is determined by the value of bit 16.
            # (if a Q1.15 value ever has >16 bits, something has gone very wrong)
        (0b11000000000000000, Q115_F_MAX_NEG),  # 0x8000
        (0b10111111111111111, Q115_F_MAX_POS),  # 0x7FFF
        (0b11000010101000000, Q115_F_MAX_NEG)   # 0x8000
    ]
)
def test_q115_to_float(q115_input, expected_float):
    result = q115_to_float(q115_input)
    assert result == expected_float


@pytest.mark.parametrize(
    ("float_input", "expected_q115"), [
        (Q115_F_MAX_POS,    0b0111111111111111),
        (-1.0,              0b1000000000000000),
        (0.5,               0b0100000000000000),
        (-0.5,              0b1100000000000000),
        (0,                 0b0),

        # below values are out of bounds, shorten to max Q1.15 regardless of value
        (1.0,               0b0111111111111111),   # (shortens to max Q115)
        (1.5,               0b0111111111111111),   # (shortens to max Q115)
        (-3,                0b1000000000000000),   # (shortens to max negative Q115)
        (-4.8347,           0b1000000000000000),   # (shortens to max negative Q115)
    ]
)
def test_float_to_q115(float_input, expected_q115):
    result = float_to_q115(float_input)
    assert result == expected_q115