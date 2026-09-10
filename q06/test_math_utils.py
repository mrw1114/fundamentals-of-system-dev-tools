# test_math_utils.py
from math_utils import calculate_price


def test_total_price():
    assert calculate_price(12.5, 4) == 50.0