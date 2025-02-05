import pytest
import numpy as np
from unittest.mock import patch
from agent import Agent
from config import INITIAL_AGENT_CAPITAL, AGENT_MEMORY_SIZE, INITIAL_TOKEN_PRICE

def test_agent_initialization():
    agent = Agent(1)
    assert agent.agent_id == 1
    assert agent.capital == INITIAL_AGENT_CAPITAL
    assert agent.tokens == 0.0
    assert len(agent.price_memory) == AGENT_MEMORY_SIZE
    assert np.all(agent.price_memory == INITIAL_TOKEN_PRICE)
    assert agent.last_trade_step == -1  # Assuming AGENT_TREND_DELAY = 1 in config


def test_update_memory():
    agent = Agent(1)
    agent.update_memory(10)
    assert agent.price_memory[-1] == 10
    agent.update_memory(12)
    assert agent.price_memory[-1] == 12
    assert agent.price_memory[-2] == 10

    # Test with None value (should be ignored)
    agent.update_memory(None)
    assert agent.price_memory[-1] == 12 # Should remain unchanged

@patch('agent.random.random')
@patch('agent.random.uniform')
@patch('agent.calculate_bonding_curve_price')
def test_trade(mock_calculate_price, mock_uniform, mock_random):
    agent = Agent(1)
    agent.tokens = 10
    mock_random.return_value = 0  # Force trade
    mock_uniform.return_value = 0.5  # trade_size
    mock_calculate_price.return_value = 10

    # Test buy scenario when price diff > threshold
    agent.price_memory = np.array([5.0] * (AGENT_MEMORY_SIZE -1) + [15.0]) # Example to trigger buy
    trade_type, amount = agent.trade(100, 1, {})
    assert trade_type == "buy"
    max_buy = agent.capital / (mock_calculate_price.return_value * (1 + 0.01)) # Assuming TRADING_FEE = 0.01
    assert amount == max_buy * 0.5

    # Test sell scenario
    agent.price_memory = np.array([15.0] * (AGENT_MEMORY_SIZE -1) + [5.0]) # Example to trigger sell
    trade_type, amount = agent.trade(100, 5, {}) # Different step to reset last_trade_step
    assert trade_type == "sell"
    assert amount == agent.tokens * 0.5

    # Test no trade scenario (frequency condition)
    mock_random.return_value = 1 # No trade
    trade_type, amount = agent.trade(100, 10, {})
    assert trade_type is None
    assert amount == 0

    # Test no trade scenario (delay condition)
    mock_random.return_value = 0
    agent.last_trade_step = 9
    trade_type, amount = agent.trade(100, 10, {})
    assert trade_type is None
    assert amount == 0