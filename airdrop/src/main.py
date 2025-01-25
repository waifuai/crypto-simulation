import time
import pandas as pd
from config import INITIAL_TOKENS, INITIAL_PRICE, NUM_USERS, SIMULATION_STEPS, MAX_STRATEGIES
from strategies import AIRDROP_PARAMETER_GRID, generate_airdrop_strategies
from simulation import run_simulation

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
# --- Plotting ---
best_strategy_name = df.loc[df['final_price'].idxmax(), 'airdrop_strategy_name']
print(f"\nBest Strategy (Highest Final Price): {best_strategy_name}")
print(f"  Final Price: ${df.loc[df['final_price'].idxmax(), 'final_price']:.4f}")
print(f"  Final Supply: {df.loc[df['final_price'].idxmax(), 'final_supply']:.2f}")
print(f"  Strategy Details: {df.loc[df['final_price'].idxmax(), 'strategy_details']}")
# --- Save Results ---
df.to_csv("airdrop_simulation_results.csv", index=False)

print("Results saved to airdrop_simulation_results.csv")