import pytest
from unittest.mock import patch
from simulation import SimulationState, simulation_step, global_state
from agent import Agent
from config import INITIAL_TOKEN_SUPPLY, NUM_AGENTS, TRADING_FEE

# Reset global state before each test
@pytest.fixture(autouse=True)
def reset_global_state():
    global_state.supply = INITIAL_TOKEN_SUPPLY
    global_state.agents = [Agent(i) for i in range(NUM_AGENTS)]

def test_simulation_state_initialization():
    state = SimulationState()
    assert state.supply == INITIAL_TOKEN_SUPPLY
    assert len(state.agents) == NUM_AGENTS

@patch('simulation.calculate_bonding_curve_price')
@patch('agent.Agent.trade')
def test_simulation_step(mock_trade, mock_calculate_price):
    mock_calculate_price.return_value = 10
    mock_trade.return_value = (None, 0)

    # No trades
    supply, capitals, tokens, price = simulation_step(1, {})
    assert supply == INITIAL_TOKEN_SUPPLY
    assert price == 10

    # Buy trade
    mock_trade.return_value = ("buy", 1)
    mock_calculate_price.return_value = 10
    supply, capitals, tokens, price = simulation_step(2, {})
    assert supply == INITIAL_TOKEN_SUPPLY + 1
    assert global_state.agents[0].capital == 989.9  # Assuming INITIAL_AGENT_CAPITAL = 1000 and TRADING_FEE = 0.01
    assert global_state.agents[0].tokens == 1

    # Sell trade
    mock_trade.return_value = ("sell", 1)
    mock_calculate_price.return_value = 20 # Increased price
    global_state.agents[0].tokens = 2 # Give agent some tokens
    supply, capitals, tokens, price = simulation_step(3, {})
    assert supply == INITIAL_TOKEN_SUPPLY + 1 - 1
    assert global_state.agents[0].capital == 989.9 + (20 * (1-TRADING_FEE)) # Check updated capital
    assert global_state.agents[0].tokens == 1 # Check updated tokens

    # Agent doesn't have enough capital
    mock_trade.return_value = ("buy", 100)
    mock_calculate_price.return_value = 1000
    old_capital = global_state.agents[0].capital
    supply, capitals, tokens, price = simulation_step(4, {})
    assert global_state.agents[0].capital == old_capital # Capital should not change
    assert global_state.agents[0].tokens == 1 # Tokens should not change
    assert supply == INITIAL_TOKEN_SUPPLY