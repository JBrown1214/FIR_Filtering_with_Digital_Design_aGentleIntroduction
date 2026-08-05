from goldenModel.qFormat_conversions import qFormat_to_float, float_to_qFormat
import pytest 
from goldenModel.qFormat_conversions import *


@pytest.mark.parametrize(
    ( "qFormat_input", "expected_float"), [
        (0b0111111111111111, qFormat_F_MAX_POS),   # 0x7FFF
        (0b1000000000000000, qFormat_F_MAX_NEG),   # 0x8000
        (0b0100000000000000,  0.5),             # 0x4000
        (0b1100000000000000, -0.5),             # 0xC000
        (0b0000000000000000, 0),                # 0x0000
    ]
)
def test_qFormat_to_float(qFormat_input, expected_float):
    result = qFormat_to_float(qFormat_input)
    assert result == expected_float


@pytest.mark.parametrize(
    ("float_input", "expected_qFormat"), [
        (qFormat_F_MAX_POS,    0b0111111111111111),
        (-1.0,              0b1000000000000000),
        (0.5,               0b0100000000000000),
        (-0.5,              0b1100000000000000),
        (0,                 0b0),
    ]
)
def test_float_to_qFormat(float_input, expected_qFormat):
    result = float_to_qFormat(float_input)
    assert result == expected_qFormat