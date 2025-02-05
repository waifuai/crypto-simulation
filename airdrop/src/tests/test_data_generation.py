import pytest
import numpy as np
from data_generation import generate_user_activity, generate_price_data

def test_generate_user_activity():
    activity = generate_user_activity(100, 0.5)
    assert len(activity) == 100
    assert all(0 <= a <= 1 for a in activity)

def test_generate_price_data():
    prices = generate_price_data(100, 1.0, 0.1, 0.05)
    assert len(prices) == 100
    assert all(p > 0 for p in prices)
