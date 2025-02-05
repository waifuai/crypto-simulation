import pytest
from config import INITIAL_TOKENS, INITIAL_PRICE, NUM_USERS, SIMULATION_STEPS

def test_config_values():
    assert INITIAL_TOKENS > 0
    assert INITIAL_PRICE > 0
    assert NUM_USERS > 0
    assert SIMULATION_STEPS > 0
