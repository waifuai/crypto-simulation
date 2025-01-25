import tensorflow as tf
import numpy as np
import time
import matplotlib.pyplot as plt
import random
import os

# --- Configuration ---
NUM_AGENTS = 100  # Reduced for faster optimization
SIMULATION_STEPS = 500  # Reduced for faster optimization
INITIAL_TOKEN_SUPPLY = 100.0
INITIAL_AGENT_CAPITAL = 100.0
INITIAL_TOKEN_PRICE = 1.0
TRADING_FEE = 0.001

BONDING_CURVE_TYPE = 'sigmoid'  # Default for initial setup

# Agent Trading Params (keeping these constant for now)
AGENT_TRADE_FREQUENCY = 0.1
AGENT_TRADE_SIZE_RANGE = [0.01, 0.1]
AGENT_MEMORY_SIZE = 10
AGENT_TREND_THRESHOLD = 0.01
AGENT_TREND_DELAY = 2

# --- Model Definition ---
# --- Bonding Curve Functions ---
def calculate_bonding_curve_price(supply, params):
    supply = tf.cast(supply, tf.float32)
    curve_type = params.get('type', 'linear')  # Default to linear if type is missing

    if curve_type == 'linear':
        m = params.get('m', 0.1)
        b = params.get('b', INITIAL_TOKEN_PRICE)
        return m * supply + b
    elif curve_type == 'exponential':
        a = params.get('a', 0.1)
        k = params.get('k', 0.01)
        return a * tf.exp(k * supply)
    elif curve_type == 'sigmoid':
        k = params.get('k', 0.02)
        s0 = params.get('s0', 100)
        k_max = params.get('k_max', 10)
        return k_max / (1 + tf.exp(-k * (supply - s0)))
    elif curve_type == 'multi-segment':
        breakpoint = params.get('breakpoint', 200)
        m = params.get('m', 0.05)
        a = params.get('a', 0.1)
        k = params.get('k', 0.02)
        lin = m * tf.minimum(supply, breakpoint)
        exp = a * tf.exp(k * tf.maximum(supply - breakpoint, 0))
        return lin + exp
    else:
        raise ValueError("Invalid bonding curve type")

# --- Agent State ---
class Agent:
    def __init__(self, agent_id):
        self.agent_id = agent_id
        self.capital = tf.Variable(INITIAL_AGENT_CAPITAL, dtype=tf.float32)
        self.tokens = tf.Variable(0.0, dtype=tf.float32)
        self.price_memory = tf.Variable(tf.zeros(AGENT_MEMORY_SIZE, dtype=tf.float32))
        self.last_trade_step = tf.Variable(-AGENT_TREND_DELAY, dtype=tf.int32)

    def update_memory(self, current_price):
        self.price_memory.assign(tf.concat([self.price_memory[1:], [current_price]], axis=0))

    def trade(self, current_supply, current_step, bonding_curve_params):
        if random.random() < AGENT_TRADE_FREQUENCY and current_step > (self.last_trade_step + AGENT_TREND_DELAY):
            trade_size = random.uniform(
                AGENT_TRADE_SIZE_RANGE[0], AGENT_TRADE_SIZE_RANGE[1]
            )

            current_price = calculate_bonding_curve_price(current_supply, bonding_curve_params)

            if tf.reduce_sum(self.price_memory) != 0.0:
                average_price = tf.reduce_mean(self.price_memory[:-1])
                price_diff = (self.price_memory[-1] - average_price) / average_price
                if price_diff > AGENT_TREND_THRESHOLD:
                    max_buy_tokens = self.capital / (current_price * (1 + TRADING_FEE))
                    tokens_to_buy = max_buy_tokens * trade_size
                    self.last_trade_step.assign(current_step)
                    return "buy", tokens_to_buy
                elif price_diff < -AGENT_TREND_THRESHOLD and self.tokens > 0:
                    tokens_to_sell = self.tokens * trade_size
                    self.last_trade_step.assign(current_step)
                    return "sell", tokens_to_sell

            if self.capital > 0:
                max_buy_tokens = self.capital / (current_price * (1 + TRADING_FEE))
                tokens_to_buy = max_buy_tokens * trade_size
                self.last_trade_step.assign(current_step)
                return "buy", tokens_to_buy

            elif self.tokens > 0:
                tokens_to_sell = self.tokens * trade_size
                self.last_trade_step.assign(current_step)
                return "sell", tokens_to_sell

        return None, 0

# --- Global State ---
supply = tf.Variable(INITIAL_TOKEN_SUPPLY, dtype=tf.float32)
agents = [] # Agents will be created per simulation run

# --- Simulation Step ---
def simulation_step(current_step, bonding_curve_params):
    global supply, agents
    trades = []
    current_price = calculate_bonding_curve_price(supply, bonding_curve_params)

    for agent in agents:
        agent.update_memory(current_price)

    for agent in agents:
        trade_type, trade_amount = agent.trade(supply, current_step, bonding_curve_params)
        if trade_type is not None:
            trades.append((agent, trade_type, trade_amount))

    for agent, trade_type, trade_amount in trades:
        if trade_type == "buy":
            price = calculate_bonding_curve_price(supply, bonding_curve_params) * (1 + TRADING_FEE)
            cost = trade_amount * price
            if agent.capital >= cost:
                agent.capital.assign_sub(cost)
                agent.tokens.assign_add(trade_amount)
                supply.assign_add(trade_amount)

        elif trade_type == "sell":
            price = calculate_bonding_curve_price(supply, bonding_curve_params) * (1 - TRADING_FEE)
            revenue = trade_amount * price
            agent.capital.assign_add(revenue)
            agent.tokens.assign_sub(trade_amount)
            supply.assign_sub(trade_amount)

    return supply, [agent.capital for agent in agents], [
        agent.tokens for agent in agents
    ], current_price

# --- Objective Function ---
def evaluate_parameters(params, num_runs=1):
    all_price_histories = []
    for _ in range(num_runs):
        global supply, agents
        supply = tf.Variable(INITIAL_TOKEN_SUPPLY, dtype=tf.float32)
        agents = [Agent(i) for i in range(NUM_AGENTS)] # Create agents for each run

        price_history = []
        for step in range(SIMULATION_STEPS):
            _, _, _, current_price = simulation_step(step, params)
            price_history.append(current_price.numpy())
        all_price_histories.append(price_history)

    # Calculate the average standard deviation of the price
    std_devs = [np.std(ph) for ph in all_price_histories]
    return np.mean(std_devs) # We want to minimize price volatility

# --- Optimization Function ---
def optimize_bonding_curve(curve_type, n_trials=10):
    best_params = None
    best_objective_value = float('inf') # Lower standard deviation is better

    print(f"Starting optimization for {curve_type} bonding curve...")

    for i in range(n_trials):
        print(f"Optimization Trial {i+1}/{n_trials}")
        if curve_type == 'linear':
            params = {
                'type': 'linear',
                'm': random.uniform(0.01, 0.2),
                'b': random.uniform(0.5, 2.0)
            }
        elif curve_type == 'exponential':
            params = {
                'type': 'exponential',
                'a': random.uniform(0.01, 0.2),
                'k': random.uniform(0.005, 0.02)
            }
        elif curve_type == 'sigmoid':
            params = {
                'type': 'sigmoid',
                'k': random.uniform(0.01, 0.05),
                's0': random.uniform(50, 150),
                'k_max': random.uniform(5, 15)
            }
        elif curve_type == 'multi-segment':
            params = {
                'type': 'multi-segment',
                'breakpoint': random.uniform(100, 300),
                'm': random.uniform(0.01, 0.1),
                'a': random.uniform(0.01, 0.2),
                'k': random.uniform(0.01, 0.03)
            }
        else:
            raise ValueError("Invalid bonding curve type for optimization")

        objective_value = evaluate_parameters(params, num_runs=1) # Consider increasing num_runs for more robust evaluation

        print(f"  Trial {i+1} - Parameters: {params}, Price Std Dev: {objective_value:.4f}")

        if objective_value < best_objective_value:
            best_objective_value = objective_value
            best_params = params
            print(f"  New best parameters found with Std Dev: {best_objective_value:.4f}")

    print(f"Optimization for {curve_type} complete.")
    print(f"Best Parameters: {best_params}")
    return best_params

# --- Main Execution ---
if __name__ == "__main__":
    # Choose the bonding curve type to optimize
    OPTIMIZE_CURVE_TYPE = 'sigmoid' # Example: Optimize the sigmoid curve

    optimal_params = optimize_bonding_curve(OPTIMIZE_CURVE_TYPE, n_trials=20)

    # --- Simulate with Optimal Parameters ---
    print(f"\nSimulating with optimal parameters for {OPTIMIZE_CURVE_TYPE}: {optimal_params}")

    BONDING_CURVE_TYPE = OPTIMIZE_CURVE_TYPE # Set the global variable for plotting
    supply = tf.Variable(INITIAL_TOKEN_SUPPLY, dtype=tf.float32)
    agents = [Agent(i) for i in range(NUM_AGENTS)]
    supply_history = []
    price_history = []
    agent_capital_history = []
    agent_token_history = []
    all_agent_capital_history = []
    all_agent_token_history = []
    start_time = time.time()

    for step in range(SIMULATION_STEPS):
        current_supply, agent_capitals, agent_tokens, current_price = simulation_step(step, optimal_params)
        supply_history.append(current_supply.numpy())
        price_history.append(current_price.numpy())
        agent_capital_history.append([c.numpy() for c in agent_capitals])
        agent_token_history.append([t.numpy() for t in agent_tokens])
        all_agent_capital_history.append(np.array([c.numpy() for c in agent_capitals]))
        all_agent_token_history.append(np.array([t.numpy() for t in agent_tokens]))

        if (step + 1) % 500 == 0:
            current_time = time.time()
            elapsed_time = current_time - start_time
            print(
                f"Step {step + 1}/{SIMULATION_STEPS} | Elapsed: {elapsed_time:.2f}s | Supply: {current_supply.numpy():.2f} | Price: {current_price.numpy():.2f} | Avg. Capital: {tf.reduce_mean([c.numpy() for c in agent_capitals]):.2f} | Avg. Tokens: {tf.reduce_mean([t.numpy() for t in agent_tokens]):.2f}"
            )

    print("Simulation with optimal parameters complete.")
    end_time = time.time()
    total_time = end_time - start_time
    print(f"Total simulation time: {total_time:.2f} seconds")

    # --- Analysis and Visualization ---
    supply_history = np.array(supply_history)
    price_history = np.array(price_history)
    agent_capital_history = np.array(agent_capital_history)
    agent_token_history = np.array(agent_token_history)
    all_agent_capital_history = np.array(all_agent_capital_history)
    all_agent_token_history = np.array(all_agent_token_history)


    # Plot token supply over time
    plt.figure(figsize=(12, 6))
    plt.plot(supply_history)
    plt.title(f"Token Supply Over Time (Optimal {OPTIMIZE_CURVE_TYPE})")
    plt.xlabel("Simulation Step")
    plt.ylabel("Token Supply")
    plt.savefig("optimal_token_supply.png")

    # Plot token price over time
    plt.figure(figsize=(12, 6))
    plt.plot(price_history)
    plt.title(f"Token Price Over Time (Optimal {OPTIMIZE_CURVE_TYPE})")
    plt.xlabel("Simulation Step")
    plt.ylabel("Token Price")
    plt.savefig("optimal_token_price.png")

    # Plot average agent capital over time
    plt.figure(figsize=(12, 6))
    plt.plot(np.mean(agent_capital_history, axis=1))
    plt.title(f"Average Agent Capital Over Time (Optimal {OPTIMIZE_CURVE_TYPE})")
    plt.xlabel("Simulation Step")
    plt.ylabel("Average Agent Capital")
    plt.savefig("optimal_agent_capital.png")

    # Plot average agent token over time
    plt.figure(figsize=(12, 6))
    plt.plot(np.mean(agent_token_history, axis=1))
    plt.title(f"Average Agent Tokens Over Time (Optimal {OPTIMIZE_CURVE_TYPE})")
    plt.xlabel("Simulation Step")
    plt.ylabel("Average Agent Tokens")
    plt.savefig("optimal_agent_tokens.png")

    # Plot wealth distribution over time
    num_timepoints_to_plot = 5
    timepoints = np.linspace(0, len(all_agent_capital_history) - 1, num_timepoints_to_plot, dtype=int)

    fig, axs = plt.subplots(2, num_timepoints_to_plot, figsize=(18, 10))

    for i, timepoint in enumerate(timepoints):
        axs[0, i].hist(all_agent_capital_history[timepoint], bins=30, color='skyblue', edgecolor='black')
        axs[0, i].set_title(f'Capital Dist. at Step {timepoint}')
        axs[0, i].set_xlabel('Capital')
        axs[0, i].set_ylabel('Frequency')

        axs[1, i].hist(all_agent_token_history[timepoint], bins=30, color='lightgreen', edgecolor='black')
        axs[1, i].set_title(f'Token Dist. at Step {timepoint}')
        axs[1, i].set_xlabel('Tokens')
        axs[1, i].set_ylabel('Frequency')

    plt.tight_layout()
    plt.savefig("optimal_wealth_distribution.png")

    print(
        f"Plots with optimal {OPTIMIZE_CURVE_TYPE} parameters saved to optimal_token_supply.png, optimal_token_price.png, optimal_agent_capital.png, optimal_agent_tokens.png, and optimal_wealth_distribution.png"
    )