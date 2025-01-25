import numpy as np
from helpers import dynamic_vesting, calculate_buy_sell_probabilities
from config import SIMULATION_STEPS, INITIAL_PRICE, INITIAL_TOKENS

# --- Simulation Step ---
def simulate_step(holdings, buy_probability, sell_probability, total_supply, price, airdrop_per_user, step, user_activity, vesting, vesting_periods, price_threshold, activity_threshold, initial_price, initial_tokens, user_params):
    if vesting != "none":
        holdings = dynamic_vesting(holdings, airdrop_per_user, price, {"vesting": vesting, "vesting_periods": vesting_periods, "price_threshold": price_threshold, "activity_threshold": activity_threshold}, step, user_activity)

    buy_decisions = np.random.uniform(size=holdings.shape) < buy_probability
    sell_decisions = np.random.uniform(size=holdings.shape) < sell_probability

    # Add gas fee impact
    gas_fee = 0.001 * price  # Dynamic gas pricing
    effective_buy_price = price + gas_fee
    effective_sell_price = price - gas_fee

    # Modify demand/supply calculations
    demand = np.sum(buy_decisions * effective_buy_price * user_activity)
    supply = np.sum(sell_decisions * effective_sell_price * holdings * user_activity)

    # Add liquidity-sensitive price impact
    liquidity_pool = 0.05 * INITIAL_TOKENS  # Constant product AMM-like
    price_impact = (demand - supply) / liquidity_pool
    new_price = price * np.exp(price_impact * 0.1)  # Exponential curve
    new_price += np.random.normal(0, 0.005 * price)  # Volatility scaling
    new_price = np.maximum(new_price, 0.000001)

    buy_amount = np.minimum(buy_decisions * (price * 50.0), total_supply * 0.005)
    sell_amount = sell_decisions * holdings
    new_holdings = holdings + buy_amount - sell_amount

    transaction_volume = np.sum(buy_amount + sell_amount)
    burn_rate = 0.05
    new_total_supply = total_supply - transaction_volume * burn_rate

    # Add activity evolution based on market conditions
    activity_change = np.where(
        price > initial_price,
        np.random.normal(0.5, 0.2, size=user_activity.shape),
        np.random.normal(-0.3, 0.2, size=user_activity.shape)
    )
    user_activity = np.clip(user_activity * (1 + activity_change), 5, 200)


    # Whale Detection System
    whale_threshold = 0.01 * INITIAL_TOKENS
    whales = holdings > whale_threshold
    if np.any(whales):
        # Apply whale-specific behavior modifiers
        user_params[whales, 1] *= 0.8  # Reduce sell probability
        user_params[whales, 3] *= 1.2  # Increase market influence


    return new_holdings, new_price, new_total_supply, user_activity  # Update return value

# --- Main Simulation Loop ---
def run_simulation(airdrop_strategy, num_users, simulation_steps, initial_tokens, initial_price, market_sentiment):
    from data_prep import assign_user_parameters
    from data_generation import generate_user_data

    user_params = assign_user_parameters(num_users)
    airdrop_distribution, user_activity = generate_user_data(num_users, airdrop_strategy, user_params)

    holdings = np.copy(airdrop_distribution)
    total_supply = float(initial_tokens)
    price = float(initial_price)

    airdrop_per_user = np.copy(airdrop_distribution)
    vesting = airdrop_strategy.get("vesting", "none")
    vesting_periods = airdrop_strategy.get("vesting_periods", 1)
    price_threshold = airdrop_strategy.get("price_threshold", 0.015)
    activity_threshold = airdrop_strategy.get("activity_threshold", 50)

    price_history = []
    market_sentiment_history = []
    initial_market_sentiment = float(market_sentiment)

    for step in range(simulation_steps):
        buy_probability, sell_probability = calculate_buy_sell_probabilities(user_params, price, initial_price, initial_market_sentiment, airdrop_strategy, holdings, step)
        holdings, price, total_supply, user_activity = simulate_step(holdings, buy_probability, sell_probability, total_supply, price, airdrop_per_user, step, user_activity, vesting, vesting_periods, price_threshold, activity_threshold, initial_price, initial_tokens, user_params)

        if step % 1024 == 0:
            price_history.append(price)
            market_sentiment_history.append(initial_market_sentiment)

        # Add price/supply impact on sentiment
        price_change = (price - initial_price) / initial_price
        supply_change = (total_supply - initial_tokens) / initial_tokens

        sentiment_change = (
            0.4 * price_change +
            0.2 * -supply_change +
            np.random.normal(0, 0.01)
        )
        new_market_sentiment = np.clip(initial_market_sentiment + sentiment_change, -1, 1)


        market_sentiment_change = np.random.normal(scale=0.01)
        new_market_sentiment = initial_market_sentiment + market_sentiment_change
        new_market_sentiment = np.clip(new_market_sentiment, -0.5, 0.5)
        initial_market_sentiment = new_market_sentiment

    return price_history, total_supply, market_sentiment_history