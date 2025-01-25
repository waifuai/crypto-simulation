import numpy as np
import time
import pandas as pd
import itertools
import matplotlib.pyplot as plt
import random

# --- Model Parameters ---
INITIAL_TOKENS = 1_000_000_000
INITIAL_PRICE = 0.10
NUM_USERS = 100  # Reduced for CPU
SIMULATION_STEPS = 1024 * 8 * 8 * 64  # Further reduced for CPU
MAX_STRATEGIES = 5  # Added parameter to limit strategies

# --- User Archetypes ---
USER_ARCHETYPES = {
    "SPECULATOR": {"base_buy_prob": 0.6, "base_sell_prob": 0.9, "price_sensitivity": 0.8, "market_influence": 0.7},
    "HODLER": {"base_buy_prob": 0.2, "base_sell_prob": 0.1, "price_sensitivity": 0.2, "market_influence": 0.3},
    "AIRDROP_HUNTER": {"base_buy_prob": 0.1, "base_sell_prob": 0.95, "price_sensitivity": 0.5, "market_influence": 0.6},
    "ACTIVE_USER": {"base_buy_prob": 0.4, "base_sell_prob": 0.3, "price_sensitivity": 0.4, "market_influence": 0.5},
}

# --- Airdrop Strategies Parameter Grid ---
AIRDROP_PARAMETER_GRID = {
    "type": ["lottery"],
    "percentage": [0.05, 0.1],
    "vesting": ["dynamic_activity"],
    "vesting_periods": [1, 3, 6, 12, 24],
    "criteria": ["holdings", "activity"],
    "thresholds": {
        "holdings": [[0.01, 0.1, 0.5, 1.0], [0.05, 0.2, 0.6, 1.2], [0.1, 0.3, 0.7, 1.5]],
        "activity": [[10, 30, 50, 100], [20, 40, 70, 120], [30, 60, 90, 150]]
    },
    "weights": [[0.1, 0.2, 0.3, 0.4], [0.2, 0.3, 0.3, 0.2], [0.4, 0.3, 0.2, 0.1]],
    "winners_fraction": [0.01, 0.02, 0.05, 0.1],
    "price_threshold": [0.015, 0.02, 0.025, 0.03],
    "activity_threshold": [30, 50, 70, 90]
}

# --- Function to Generate Airdrop Strategies ---
def generate_airdrop_strategies(param_grid, max_strategies):
    keys = list(param_grid.keys())
    strategies = []

    tiered_combinations = []
    non_tiered_keys = [k for k in keys if k not in ("thresholds", "weights")]

    if "type" in param_grid and "tiered" in param_grid["type"]:
        tiered_indices = [i for i, val in enumerate(param_grid["type"]) if val == "tiered"]

        for type_index in tiered_indices:
            temp_grid = {k: param_grid[k] for k in non_tiered_keys}
            temp_grid["type"] = ["tiered"]
            temp_grid["criteria"] = [c for c in param_grid["criteria"] if c != "none"]

            for combo in itertools.product(*[temp_grid[k] for k in temp_grid]):
                strategy = dict(zip(temp_grid.keys(), combo))
                criteria_value = strategy["criteria"]
                threshold_options = param_grid["thresholds"][criteria_value]
                weight_options = param_grid["weights"]

                for threshold, weight in itertools.product(threshold_options, weight_options):
                    new_strategy = strategy.copy()
                    new_strategy["thresholds"] = threshold
                    new_strategy["weights"] = weight
                    new_strategy["criteria"] = criteria_value
                    tiered_combinations.append(new_strategy)

    other_combinations = []
    non_tiered_keys = [k for k in keys if k not in ("thresholds", "weights")]
    temp_grid = {k: param_grid[k] for k in non_tiered_keys}

    for combo in itertools.product(*[temp_grid[k] for k in non_tiered_keys]):
        strategy = dict(zip(non_tiered_keys, combo))
        if strategy["type"] != "tiered":
            other_combinations.append(strategy)

    all_combinations = tiered_combinations + other_combinations
    random.shuffle(all_combinations)

    for strategy in all_combinations:
        if len(strategies) >= max_strategies:
            break

        if strategy["type"] == "tiered" and strategy["criteria"] == "none":
            continue

        strategies.append(strategy)

    for i, strategy in enumerate(strategies):
        strategy["name"] = f"Strategy_{i+1}"

    return strategies

# --- Data Preparation ---
# --- User Archetypes Data ---
user_archetypes_data = []
for archetype, params in USER_ARCHETYPES.items():
    user_archetypes_data.append([params["base_buy_prob"], params["base_sell_prob"], params["price_sensitivity"], params["market_influence"]])
user_archetypes_array = np.array(user_archetypes_data, dtype=np.float32)

# --- Helper Functions ---
def assign_user_parameters(num_users):
    archetype_probs = [0.2, 0.4, 0.1, 0.3]
    archetypes = np.random.choice(len(archetype_probs), size=num_users, p=archetype_probs)
    user_params = user_archetypes_array[archetypes]

    noise_scale = 0.1
    noise = np.random.normal(size=user_params.shape, scale=noise_scale)
    user_params = user_params + noise
    user_params = np.clip(user_params, 0.0, 1.0)
    return user_params

def calculate_buy_sell_probabilities(user_params, current_price, initial_price, market_sentiment, airdrop_strategy, holdings):
    airdrop_price = airdrop_strategy.get("airdrop_price", initial_price)

    base_buy_prob = user_params[:, 0]
    base_sell_prob = user_params[:, 1]

    if airdrop_strategy["type"] == "tiered" and airdrop_strategy["criteria"] == "holdings":
        base_sell_prob = base_sell_prob * 0.5

    price_sensitivity = user_params[:, 2]
    market_influence = user_params[:, 3]

    price_change_factor = (current_price - initial_price) / initial_price

    exponent_buy = -(base_buy_prob + price_sensitivity * (initial_price - current_price) + market_influence * market_sentiment - price_change_factor * 0.5)
    exponent_buy = np.clip(exponent_buy, -50, 50)
    buy_prob = 1 / (1 + np.exp(exponent_buy))

    exponent_sell = -(base_sell_prob - price_sensitivity * (current_price - airdrop_price) + market_influence * market_sentiment + price_change_factor * 0.3)
    exponent_sell = np.clip(exponent_sell, -50, 50)
    sell_prob = 1 / (1 + np.exp(exponent_sell))

    sell_prob = np.where(holdings > 0, sell_prob * (1 + np.log(holdings + 1)), sell_prob)

    return buy_prob, sell_prob

def dynamic_vesting(holdings, airdrop_per_user, current_price, airdrop_strategy, step, user_activity):
    vesting_type = airdrop_strategy["vesting"]
    vesting_periods = airdrop_strategy.get("vesting_periods", 1)

    dynamic_price_mask = vesting_type == "dynamic_price"
    dynamic_activity_mask = vesting_type == "dynamic_activity"
    linear_vesting_mask = vesting_type == "linear"

    vested_amount = np.zeros_like(holdings)

    if dynamic_price_mask:
        price_threshold = airdrop_strategy["price_threshold"]
        mask = ((step % (SIMULATION_STEPS // vesting_periods)) == 0) & (current_price > price_threshold)
        vested_amount = np.where(mask, airdrop_per_user / vesting_periods, 0.0)

    elif dynamic_activity_mask:
        activity_threshold = airdrop_strategy["activity_threshold"]
        mask = ((step % (SIMULATION_STEPS // vesting_periods)) == 0) & (user_activity >= activity_threshold)
        vested_amount = np.where(mask, airdrop_per_user / vesting_periods, 0.0)

    elif linear_vesting_mask:
         mask = (step % (SIMULATION_STEPS // vesting_periods)) == 0
         vested_amount = np.where(mask, airdrop_per_user / vesting_periods, 0.0)

    return holdings + vested_amount

# --- Data Generation ---
def generate_user_data(num_users, airdrop_strategy, user_params):
    initial_holdings = np.zeros(num_users)
    user_activity = np.random.poisson(lam=20.0, size=num_users).astype(np.float32)
    user_activity = user_activity + np.random.uniform(low=0, high=5, size=num_users)

    airdrop_amount = INITIAL_TOKENS * airdrop_strategy["percentage"]

    if airdrop_strategy["type"] == "none":
        eligibility = np.zeros(num_users)
    elif airdrop_strategy["type"] == "uniform":
        eligibility = np.ones(num_users)
    elif airdrop_strategy["type"] == "tiered":
        if airdrop_strategy["criteria"] == "holdings":
            criteria_values = initial_holdings
        elif airdrop_strategy["criteria"] == "activity":
            criteria_values = user_activity
        else:
            criteria_values = np.zeros(num_users)

        thresholds = np.array(airdrop_strategy["thresholds"], dtype=np.float32)
        weights = np.array(airdrop_strategy["weights"], dtype=np.float32)

        eligibility = np.sum(np.where(criteria_values[:, np.newaxis] >= thresholds, weights, 0.0), axis=1)

    elif airdrop_strategy["type"] == "lottery":
        num_winners = int(num_users * airdrop_strategy["winners_fraction"])
        winners = np.random.choice(num_users, size=num_winners, replace=False)
        eligibility = np.zeros(num_users)
        eligibility[winners] = 1
    else:
        eligibility = np.zeros(num_users)

    airdrop_distribution = np.where(
      eligibility > 0,
      airdrop_amount * eligibility / np.sum(eligibility),
      0.0
    )

    return airdrop_distribution, user_activity

# --- Simulation Step ---
def simulate_step(holdings, buy_probability, sell_probability, total_supply, price, airdrop_per_user, step, user_activity, vesting, vesting_periods, price_threshold, activity_threshold):
    if vesting != "none":
        holdings = dynamic_vesting(holdings, airdrop_per_user, price, {"vesting": vesting, "vesting_periods": vesting_periods, "price_threshold": price_threshold, "activity_threshold": activity_threshold}, step, user_activity)

    buy_decisions = np.random.uniform(size=holdings.shape) < buy_probability
    sell_decisions = np.random.uniform(size=holdings.shape) < sell_probability

    demand = np.sum(buy_decisions * price)
    supply = np.sum(sell_decisions * holdings * price)

    price_change = (demand - supply) / total_supply
    price_change_multiplier = np.maximum(0.1, np.abs(demand - supply) / total_supply * 15.0)
    new_price = np.maximum(price + price_change * price_change_multiplier, price * 0.2)
    new_price = new_price + np.random.normal(scale=0.01)
    new_price = np.maximum(new_price, 0.000001)

    buy_amount = np.minimum(buy_decisions * (price * 50.0), total_supply * 0.005)
    sell_amount = sell_decisions * holdings
    new_holdings = holdings + buy_amount - sell_amount

    transaction_volume = np.sum(buy_amount + sell_amount)
    burn_rate = 0.05
    new_total_supply = total_supply - transaction_volume * burn_rate

    return new_holdings, new_price, new_total_supply, user_activity

# --- Main Simulation Loop ---
def run_simulation(airdrop_strategy, num_users, simulation_steps, initial_tokens, initial_price, market_sentiment):
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
        buy_probability, sell_probability = calculate_buy_sell_probabilities(user_params, price, initial_price, initial_market_sentiment, airdrop_strategy, holdings)
        holdings, price, total_supply, user_activity = simulate_step(holdings, buy_probability, sell_probability, total_supply, price, airdrop_per_user, step, user_activity, vesting, vesting_periods, price_threshold, activity_threshold)

        if step % 1024 == 0:
            price_history.append(price)
            market_sentiment_history.append(initial_market_sentiment)

        market_sentiment_change = np.random.normal(scale=0.01)
        new_market_sentiment = initial_market_sentiment + market_sentiment_change
        new_market_sentiment = np.clip(new_market_sentiment, -0.5, 0.5)
        initial_market_sentiment = new_market_sentiment

    return price_history, total_supply, market_sentiment_history

# --- Main Execution Block ---
AIRDROP_STRATEGIES = generate_airdrop_strategies(AIRDROP_PARAMETER_GRID, MAX_STRATEGIES)

all_results = []
start_time = time.time()

for airdrop_strategy in AIRDROP_STRATEGIES:
    airdrop_name = airdrop_strategy["name"]
    print(f"Running simulation for: {airdrop_name}")
    print(f"  Strategy Details: {airdrop_strategy}")

    price_history, final_supply, market_sentiment_history = run_simulation(airdrop_strategy, NUM_USERS, SIMULATION_STEPS, INITIAL_TOKENS, INITIAL_PRICE, 0.0)

    result = {
        "airdrop_strategy_name": airdrop_name,
        "final_price": price_history[-1],
        "price_history": price_history,
        "final_supply": final_supply,
        "market_sentiment_history": market_sentiment_history,
        "strategy_details": str(airdrop_strategy)
    }
    all_results.append(result)

end_time = time.time()
print(f"Simulation took {end_time - start_time:.2f} seconds")

# --- Create DataFrame ---
df = pd.DataFrame(all_results)

# --- Plotting ---
best_strategy_name = df.loc[df['final_price'].idxmax(), 'airdrop_strategy_name']
print(f"\nBest Strategy (Highest Final Price): {best_strategy_name}")
print(f"  Final Price: ${df.loc[df['final_price'].idxmax(), 'final_price']:.4f}")
print(f"  Final Supply: {df.loc[df['final_price'].idxmax(), 'final_supply']:.2f}")
print(f"  Strategy Details: {df.loc[df['final_price'].idxmax(), 'strategy_details']}")

plt.figure(figsize=(12, 8))

for index, row in df.iterrows():
    plt.plot(row["price_history"], label=row['airdrop_strategy_name'])

plt.title("Token Price Simulation Under Different Airdrop Strategies")
plt.xlabel("Simulation Step")
plt.ylabel("Token Price")
plt.legend()
plt.grid(True)
plt.show()

# --- Save Results ---
df.to_csv("airdrop_simulation_results.csv", index=False)

print("Results saved to airdrop_simulation_results.csv")