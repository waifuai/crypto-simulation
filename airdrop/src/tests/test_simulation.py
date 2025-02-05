import pytest
import numpy as np
from simulation import simulate_step, run_simulation
from config import INITIAL_TOKENS, SIMULATION_STEPS, INITIAL_PRICE

def test_simulate_step():
    num_users = 10
    holdings = np.ones(num_users)
    buy_probability = np.ones(num_users) * 0.5
    sell_probability = np.ones(num_users) * 0.5
    total_supply = 1_000_000
    price = 0.10
    airdrop_per_user = np.ones(num_users) * 0.1
    step = 0
    user_activity = np.ones(num_users) * 20
    vesting = "none"
    vesting_periods = 1
    price_threshold = 0.015
    activity_threshold = 50
    initial_price = 0.10
    initial_tokens = 1_000_000
    user_params = np.ones((num_users, 4))
    
    new_holdings, new_price, new_total_supply, new_user_activity = simulate_step(
        holdings, buy_probability, sell_probability, total_supply, price, airdrop_per_user,
        step, user_activity, vesting, vesting_periods, price_threshold, activity_threshold,
        initial_price, initial_tokens, user_params
    )
    
    assert new_price > 0
    # Expect that some tokens are burned so total_supply should be lower.
    assert new_total_supply < total_supply

def test_run_simulation():
    airdrop_strategy = {"type": "uniform", "percentage": 0.1, "vesting": "none"}
    num_users = 10
    simulation_steps = 100
    initial_tokens = 1_000_000
    initial_price = 0.10
    market_sentiment = 0.0
    
    price_history, final_supply, market_sentiment_history = run_simulation(
        airdrop_strategy, num_users, simulation_steps, initial_tokens, initial_price, market_sentiment
    )
    # Price history is recorded every 1024 steps (including step 0), so we expect simulation_steps//1024 + 1 entries.
    expected_length = simulation_steps // 1024 + 1
    assert len(price_history) == expected_length
    assert final_supply < initial_tokens
