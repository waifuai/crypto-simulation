import time
import logging
import pandas as pd
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Strategy for CPU
strategy = tf.distribute.get_strategy()  # Default strategy for CPU/GPU
logging.info("Running on CPU/GPU.")

# Constants
NUM_SIMULATION_STEPS = 1000 * 16 * 2 * 8
NUM_TOKENS = 5
NUM_AFFILIATES = 5
INITIAL_SUPPLY = 10000
INITIAL_PRICE = 1.0
INITIAL_COMMISSION_RATE = 0.10
AFFILIATE_STARTING_POINT = 0
INITIAL_BASE_CURRENCY = 1000
INITIAL_TOKEN_INVESTMENT = 10
COMMISSION_DYNAMICS_STEP = 10
DYNAMIC_ADJUSTMENT_RATE = 0.0005  # Reduced adjustment rate
MOVING_AVERAGE_WINDOW = 50  # Increased window for smoother price adjustments
PRICE_IMPACT_FACTOR = 0.01  # Reduced impact factor
BONDING_CURVE_TYPE_CHANGE_INTERVAL = 500 # Increased interval
BONDING_CURVE_PARAM_CHANGE_INTERVAL = 150 # Reduced interval for more frequent parameter tweaks

# Variable bonding curve change intervals for each token
bonding_curve_change_intervals = np.random.choice(
    range(500, 1001), size=NUM_TOKENS, replace=True
)

# --- Bonding Curve Functions (TensorFlow Compatible) ---
def linear_bonding_curve(supply, m=0.001, b=1):
    return tf.cast(m, dtype=tf.float32) * tf.cast(supply, dtype=tf.float32) + tf.cast(
        b, dtype=tf.float32
    )

def exponential_bonding_curve(supply, a=1, k=0.0005):
    return tf.cast(a, dtype=tf.float32) * tf.exp(
        tf.cast(k, dtype=tf.float32) * tf.cast(supply, dtype=tf.float32)
    )

def sigmoid_bonding_curve(supply, K=10, k=0.001, S0=5000):
    return tf.cast(K, dtype=tf.float32) / (
        1
        + tf.exp(
            -tf.cast(k, dtype=tf.float32)
            * (tf.cast(supply, dtype=tf.float32) - tf.cast(S0, dtype=tf.float32))
        )
    )

def root_bonding_curve(supply, k=0.1):
    return tf.sqrt(tf.cast(supply, dtype=tf.float32)) * tf.cast(k, dtype=tf.float32)

def inverse_bonding_curve(supply, k=100000):
    return tf.cast(k, dtype=tf.float32) / (tf.cast(supply, dtype=tf.float32) + 1)

bonding_curve_functions = [
    linear_bonding_curve,
    exponential_bonding_curve,
    sigmoid_bonding_curve,
    root_bonding_curve,
    inverse_bonding_curve,
]

# --- Token Class ---
class Token:
    def __init__(self, name, initial_supply, initial_price, bonding_curve_func):
        self.name = name
        self.supply = tf.Variable(float(initial_supply), dtype=tf.float32)
        self.price = tf.Variable(initial_price, dtype=tf.float32)
        self.bonding_curve_func = bonding_curve_func
        self.bonding_curve_type_index = 0
        self.price_history = []
        self.supply_history = []
        self.buy_order_history = []
        self.sell_order_history = []
        self.last_price_adjustment = 0.0  # To dampen price fluctuations
        logging.info(
            f"Token {self.name} created with initial supply {initial_supply} and price {initial_price}"
        )

    def calculate_price(self):
        try:
            price_tensor = self.bonding_curve_func(self.supply)
            demand_factor = sum(self.buy_order_history[-MOVING_AVERAGE_WINDOW:]) - sum(
                self.sell_order_history[-MOVING_AVERAGE_WINDOW:]
            )
            price_adjustment = tf.math.tanh(demand_factor * PRICE_IMPACT_FACTOR) * 0.5 # Dampen the adjustment

            # Apply a smoothing factor to price adjustments
            price_adjustment = 0.5 * price_adjustment + 0.5 * self.last_price_adjustment
            self.last_price_adjustment = price_adjustment

            price_tensor *= (1 + price_adjustment)

            if price_tensor.shape.rank != 0:
                price_tensor = tf.squeeze(price_tensor)

            # Add a safety mechanism to prevent extreme price changes
            max_price_change = 0.1 * self.price.numpy()  # Limit change to 10%
            if price_tensor > self.price + max_price_change:
                price_tensor = self.price + max_price_change
            elif price_tensor < self.price - max_price_change:
                price_tensor = self.price - max_price_change

            self.price.assign(price_tensor)
            self.price_history.append(self.price.numpy())
            self.supply_history.append(self.supply.numpy())

            logging.debug(
                f"Token {self.name} price calculated. New price: {self.price.numpy()}, Supply: {self.supply.numpy()}, Demand Factor: {demand_factor}"
            )

        except Exception as e:
            logging.error(f"Error calculating price for token {self.name}: {e}")
            self.price.assign(0.0)

    def buy(self, amount):
        self.supply.assign_add(tf.cast(amount, dtype=tf.float32))
        self.calculate_price()
        self.buy_order_history.append(amount)
        if len(self.buy_order_history) > MOVING_AVERAGE_WINDOW:
            self.buy_order_history.pop(0)
        logging.debug(
            f"Token {self.name} bought. Amount: {amount}, New supply: {self.supply.numpy()}, Price: {self.price.numpy()}"
        )
        return self.price.numpy()

    def sell(self, amount):
        amount = tf.cast(amount, dtype=tf.float32)
        if amount > self.supply:
            amount = self.supply
            logging.warning(
                f"Token {self.name} sell amount exceeded supply. Selling available supply: {amount.numpy()}"
            )
        self.supply.assign_sub(amount)
        self.calculate_price()
        self.sell_order_history.append(amount)
        if len(self.sell_order_history) > MOVING_AVERAGE_WINDOW:
            self.sell_order_history.pop(0)
        logging.debug(
            f"Token {self.name} sold. Amount: {amount.numpy()}, New supply: {self.supply.numpy()}, Price: {self.price.numpy()}"
        )
        return self.price.numpy()

    def change_bonding_curve(self):
        self.bonding_curve_type_index = (
            self.bonding_curve_type_index + 1
        ) % len(bonding_curve_functions)
        self.bonding_curve_func = bonding_curve_functions[
            self.bonding_curve_type_index
        ]
        logging.info(
            f"Token {self.name} changed bonding curve to {self.bonding_curve_func.__name__}"
        )
        self.calculate_price()

    def change_bonding_curve_parameters(self):
        current_function = self.bonding_curve_func.__name__

        if current_function == "linear_bonding_curve":
            new_m = np.random.uniform(0.0005, 0.0015) # Narrowed range
            new_b = np.random.uniform(0.8, 1.2) # Narrowed range
            self.bonding_curve_func = lambda supply: linear_bonding_curve(
                supply, m=new_m, b=new_b
            )

        elif current_function == "exponential_bonding_curve":
            new_a = np.random.uniform(0.8, 1.2) # Narrowed range
            new_k = np.random.uniform(0.0002, 0.0008) # Narrowed range
            self.bonding_curve_func = lambda supply: exponential_bonding_curve(
                supply, a=new_a, k=new_k
            )

        elif current_function == "sigmoid_bonding_curve":
            new_K = np.random.uniform(9, 11) # Narrowed range
            new_k = np.random.uniform(0.0007, 0.0013) # Narrowed range
            new_S0 = np.random.uniform(4500, 5500) # Narrowed range
            self.bonding_curve_func = lambda supply: sigmoid_bonding_curve(
                supply, K=new_K, k=new_k, S0=new_S0
            )

        elif current_function == "root_bonding_curve":
            new_k = np.random.uniform(0.07, 0.15) # Narrowed range
            self.bonding_curve_func = lambda supply: root_bonding_curve(
                supply, k=new_k
            )

        elif current_function == "inverse_bonding_curve":
            new_k = np.random.uniform(90000, 110000) # Narrowed range
            self.bonding_curve_func = lambda supply: inverse_bonding_curve(
                supply, k=new_k
            )

        logging.info(
            f"Token {self.name} changed bonding curve parameters for {current_function}"
        )
        self.calculate_price()

# --- Affiliate Class ---
class Affiliate:
    def __init__(self, affiliate_id, commission_rate, is_whale=False):
        self.affiliate_id = affiliate_id
        self.commission_rate = tf.Variable(commission_rate, dtype=tf.float32)
        self.base_currency_balance = tf.Variable(float(INITIAL_BASE_CURRENCY), dtype=tf.float32)
        self.total_earned = tf.Variable(0.0, dtype=tf.float32)
        self.recent_investment = []
        self.wallet = {f"Token_{i}": tf.Variable(0.0, dtype=tf.float32) for i in range(NUM_TOKENS)}
        self.earnings_history = []
        self.commission_rate_history = []
        self.is_whale = is_whale
        self.whale_investment_capacity = tf.Variable(0.0, dtype=tf.float32)
        self.dynamic_adjustment_rate = DYNAMIC_ADJUSTMENT_RATE # Initialize here

        logging.info(
            f"Affiliate {affiliate_id} created with initial commission rate {commission_rate}, Whale: {is_whale}"
        )

    def calculate_commission(self, investment_amount):
        return tf.multiply(self.commission_rate, investment_amount)

    def calculate_dynamic_adjustment_rate(self):
        if self.total_earned < 1000:
            self.dynamic_adjustment_rate = DYNAMIC_ADJUSTMENT_RATE * 0.5
        elif self.total_earned < 5000:
            self.dynamic_adjustment_rate = DYNAMIC_ADJUSTMENT_RATE
        elif self.total_earned < 10000:
            self.dynamic_adjustment_rate = DYNAMIC_ADJUSTMENT_RATE * 1.25 # Reduced multiplier
        else:
            self.dynamic_adjustment_rate = DYNAMIC_ADJUSTMENT_RATE * 1.5  # Reduced multiplier

        logging.debug(
            f"Affiliate {self.affiliate_id}: Dynamic adjustment rate set to {self.dynamic_adjustment_rate}"
        )

    def calculate_average_investment(self):
        if not self.recent_investment:
            return 0
        return sum(self.recent_investment) / len(self.recent_investment)

    def adjust_commission_dynamically(self, step):
        if step % COMMISSION_DYNAMICS_STEP == 0:
            self.calculate_dynamic_adjustment_rate()

            if self.is_whale:
                if self.total_earned > 10000:
                    self.whale_investment_capacity.assign(self.total_earned * np.random.uniform(0.05, 0.15)) # Reduced range
                else:
                    self.whale_investment_capacity.assign(0.0)

            avg_investment = self.calculate_average_investment()
            if avg_investment > 12: # Adjusted threshold
                self.commission_rate.assign_add(self.dynamic_adjustment_rate)
                logging.debug(
                    f"Affiliate {self.affiliate_id}: Commission rate increased by {self.dynamic_adjustment_rate} to {self.commission_rate.numpy()} due to high investment"
                )
            elif avg_investment > 0:
                self.commission_rate.assign_sub(self.dynamic_adjustment_rate)
                logging.debug(
                    f"Affiliate {self.affiliate_id}: Commission rate decreased by {self.dynamic_adjustment_rate} to {self.commission_rate.numpy()} due to low investment"
                )

            if self.commission_rate > 0.18: # Reduced cap
                self.commission_rate.assign(0.18)
                logging.debug(
                    f"Affiliate {self.affiliate_id} commission rate capped to 0.18"
                )
            if self.commission_rate < 0.02: # Increased floor
                self.commission_rate.assign(0.02)
                logging.debug(
                    f"Affiliate {self.affiliate_id} commission rate floored to 0.02"
                )

# --- Simulation Logic ---
with strategy.scope():
    token_function_indices = np.random.choice(
        len(bonding_curve_functions), size=NUM_TOKENS
    )
    tokens = [
        Token(
            f"Token_{i}",
            INITIAL_SUPPLY,
            INITIAL_PRICE,
            bonding_curve_functions[token_function_indices[i]],
        )
        for i in range(NUM_TOKENS)
    ]

    affiliates = [Affiliate(i, INITIAL_COMMISSION_RATE, i < (NUM_AFFILIATES // 5)) for i in range(NUM_AFFILIATES)]

    def token_simulation_step(step):
        logging.debug(f"Starting token simulation step: {step}")
        for affiliate in affiliates:
            num_transactions = np.random.randint(1, 3) if not affiliate.is_whale else np.random.randint(0, 2) # Reduced whale transactions

            for _ in range(num_transactions):
                random_token_index = np.random.randint(NUM_TOKENS)
                token = tokens[random_token_index]

                if affiliate.is_whale and affiliate.whale_investment_capacity > 0:
                    invest_amount = affiliate.whale_investment_capacity * np.random.uniform(0.1, 0.4) # Reduced range
                else:
                    invest_amount = INITIAL_TOKEN_INVESTMENT + (np.random.rand(1)[0] * 5) # Reduced max investment

                token_price = token.price.numpy()
                if token_price > 0: # Avoid division by zero
                    tokens_to_trade = invest_amount / token_price
                else:
                    tokens_to_trade = 0
                    continue # Skip if price is zero

                if np.random.rand() < 0.6:  # Slightly adjusted probability for buy
                    cost = tokens_to_trade * token_price
                    if affiliate.base_currency_balance.numpy() >= cost:
                        token.buy(tf.cast(tokens_to_trade, dtype=tf.float32))
                        affiliate.base_currency_balance.assign_sub(tf.cast(cost, dtype=tf.float32))
                        affiliate.wallet[token.name].assign_add(tf.cast(tokens_to_trade, dtype=tf.float32))
                        logging.debug(f"Affiliate {affiliate.affiliate_id} bought {tokens_to_trade:.2f} {token.name} for {cost:.2f}")
                    else:
                        logging.debug(f"Affiliate {affiliate.affiliate_id} could not afford to buy {token.name}")
                else:
                    tokens_available = affiliate.wallet[token.name].numpy()
                    tokens_to_sell = min(tokens_to_trade, tokens_available)
                    if tokens_to_sell > 0:
                        sale_proceeds = token.sell(tf.cast(tokens_to_sell, dtype=tf.float32)) * tokens_to_sell
                        affiliate.wallet[token.name].assign_sub(tf.cast(tokens_to_sell, dtype=tf.float32))
                        affiliate.base_currency_balance.assign_add(tf.cast(sale_proceeds, dtype=tf.float32))
                        logging.debug(f"Affiliate {affiliate.affiliate_id} sold {tokens_to_sell:.2f} {token.name} for {sale_proceeds:.2f}")
                    else:
                        logging.debug(f"Affiliate {affiliate.affiliate_id} has no {token.name} to sell")

                affiliate.recent_investment.append(invest_amount)
                if len(affiliate.recent_investment) > MOVING_AVERAGE_WINDOW:
                    affiliate.recent_investment.pop(0)

        for i, token in enumerate(tokens):
            if step % bonding_curve_change_intervals[i] == 0:
                token.change_bonding_curve()

            if step % BONDING_CURVE_PARAM_CHANGE_INTERVAL == 0: # More frequent parameter changes
                token.change_bonding_curve_parameters()

        logging.debug(f"Finished token simulation step: {step}")

    def affiliate_simulation_step(step):
        logging.debug(f"Starting affiliate simulation step: {step}")
        for affiliate in affiliates:
            for token_name in list(affiliate.wallet.keys()):
                if affiliate.wallet[token_name].numpy() > 0 and np.random.rand() < 0.05: # Reduced sell frequency
                    tokens_to_sell_percentage = np.random.rand() * 0.05 # Sell up to 5%
                    tokens_to_sell = affiliate.wallet[token_name].numpy() * tokens_to_sell_percentage

                    for token in tokens:
                        if token.name == token_name:
                            sale_proceeds = token.sell(tf.cast(tokens_to_sell, dtype=tf.float32)) * token.price.numpy()
                            affiliate.wallet[token_name].assign_sub(tf.cast(tokens_to_sell, dtype=tf.float32))
                            affiliate.base_currency_balance.assign_add(tf.cast(sale_proceeds, dtype=tf.float32))
                            logging.debug(f"Affiliate {affiliate.affiliate_id} sold {tokens_to_sell:.2f} {token_name} for {sale_proceeds:.2f} (periodic sell)")
                            break

            affiliate.earnings_history.append(affiliate.total_earned.numpy())
            affiliate.commission_rate_history.append(
                affiliate.commission_rate.numpy()
            )
            affiliate.adjust_commission_dynamically(step)

        logging.debug(f"Finished affiliate simulation step: {step}")

    def run_simulation():
        token_histories = {
            token.name: {
                "price": [],
                "supply": [],
                "bonding_curve": [],
            }
            for token in tokens
        }
        affiliate_histories = {
            affiliate.affiliate_id: {
                "earned": [],
                "commission_rate": [],
                "wallet": [],
                "base_currency_balance": []
            }
            for affiliate in affiliates
        }

        start_time = time.time()
        logging.info("Simulation Started")
        for step in range(NUM_SIMULATION_STEPS):
            token_simulation_step(step)
            affiliate_simulation_step(step)

            for token in tokens:
                token_histories[token.name]["price"].append(token.price.numpy())
                token_histories[token.name]["supply"].append(token.supply.numpy())
                token_histories[token.name]["bonding_curve"].append(
                    token.bonding_curve_func.__name__
                )

            for affiliate in affiliates:
                affiliate_histories[affiliate.affiliate_id]["earned"].append(
                    affiliate.total_earned.numpy()
                )
                affiliate_histories[affiliate.affiliate_id][
                    "commission_rate"
                ].append(affiliate.commission_rate.numpy())
                affiliate_histories[affiliate.affiliate_id]["wallet"].append(
                    {
                        token_name: wallet_balance.numpy()
                        for token_name, wallet_balance in affiliate.wallet.items()
                    }
                )
                affiliate_histories[affiliate.affiliate_id]["base_currency_balance"].append(
                    affiliate.base_currency_balance.numpy()
                )

        end_time = time.time()
        logging.info(f"Simulation Completed in: {end_time - start_time:.2f} seconds")
        return token_histories, affiliate_histories

    token_histories, affiliate_histories = run_simulation()

# --- Data Analysis and Visualization ---
def analyze_results(token_histories, affiliate_histories):
    logging.info("Analyzing simulation results...")

    for token_name, history in token_histories.items():
        prices = np.array(history["price"])
        supplies = np.array(history["supply"])
        price_mean = np.mean(prices)
        price_std = np.std(prices)
        supply_mean = np.mean(supplies)
        supply_std = np.std(supplies)
        logging.info(f"Token {token_name}: Price Mean={price_mean:.2f}, Std={price_std:.2f}, Supply Mean={supply_mean:.2f}, Std={supply_std:.2f}")

    affiliate_earnings = {}
    for aff_id, history in affiliate_histories.items():
        base_currency_balances = np.array(history["base_currency_balance"])
        final_base_currency_balance = base_currency_balances[-1] if base_currency_balances.size > 0 else 0
        commission_rates = np.array(history["commission_rate"])
        final_commission_rate = commission_rates[-1] if commission_rates.size > 0 else 0
        affiliate_earnings[aff_id] = final_base_currency_balance
        logging.info(f"Affiliate {aff_id}: Final Base Currency={final_base_currency_balance:.2f}, Commission Rate={final_commission_rate:.4f}")

    return affiliate_earnings

def plot_token_simulation(token_histories):
    plt.figure(figsize=(12, 6))
    for token_name in token_histories:
        plt.plot(token_histories[token_name]["price"], label=token_name)
    plt.xlabel("Simulation Step")
    plt.ylabel("Token Price")
    plt.title("Token Prices Over Time")
    plt.legend()
    plt.show()

    plt.figure(figsize=(12, 6))
    for token_name in token_histories:
        plt.plot(token_histories[token_name]["supply"], label=token_name)
    plt.xlabel("Simulation Step")
    plt.ylabel("Token Supply")
    plt.title("Token Supply Over Time")
    plt.legend()
    plt.show()

    plt.figure(figsize=(12, 8))
    for token_name in token_histories:
        plt.plot(token_histories[token_name]["supply"], token_histories[token_name]["price"], label=token_name)
    plt.xlabel("Supply")
    plt.ylabel("Price")
    plt.title("Token Price vs Supply")
    plt.legend()
    plt.show()

def plot_affiliate_simulation(affiliate_histories, affiliates):
    plt.figure(figsize=(12, 6))
    avg_base_currency = np.mean([hist["base_currency_balance"] for hist in affiliate_histories.values()], axis=0)
    plt.plot(avg_base_currency, label="Average Base Currency")
    plt.xlabel("Simulation Step")
    plt.ylabel("Average Base Currency")
    plt.title("Average Affiliate Base Currency Over Time")
    plt.legend()
    plt.show()

    plt.figure(figsize=(12, 6))
    avg_commission_rate = np.mean([hist["commission_rate"] for hist in affiliate_histories.values()], axis=0)
    plt.plot(avg_commission_rate, label="Average Commission Rate")
    plt.xlabel("Simulation Step")
    plt.ylabel("Average Commission Rate")
    plt.title("Average Affiliate Commission Rate Over Time")
    plt.legend()
    plt.show()

    whale_balances = [affiliate_histories[i]["base_currency_balance"] for i in range(NUM_AFFILIATES) if affiliates[i].is_whale]
    non_whale_balances = [affiliate_histories[i]["base_currency_balance"] for i in range(NUM_AFFILIATES) if not affiliates[i].is_whale]

    if whale_balances:
        plt.figure(figsize=(12, 6))
        for balances in whale_balances:
            plt.plot(balances, label="Whale Base Currency")
        plt.xlabel("Simulation Step")
        plt.ylabel("Base Currency")
        plt.title("Whale Affiliate Base Currency Over Time")
        plt.legend()
        plt.show()

    if non_whale_balances:
        plt.figure(figsize=(12, 6))
        for balances in non_whale_balances:
            plt.plot(balances, label="Non-Whale Base Currency")
        plt.xlabel("Simulation Step")
        plt.ylabel("Base Currency")
        plt.title("Non-Whale Affiliate Base Currency Over Time")
        plt.legend()
        plt.show()

    if affiliate_histories:
        affiliate_id_to_plot = 0
        wallet_history = affiliate_histories[affiliate_id_to_plot]["wallet"]
        token_names = list(wallet_history[0].keys())

        plt.figure(figsize=(12, 6))
        for token_name in token_names:
            token_balance_over_time = [wallet.get(token_name, 0) for wallet in wallet_history]
            plt.plot(token_balance_over_time, label=token_name)
        plt.xlabel("Simulation Step")
        plt.ylabel("Token Balance")
        plt.title(f"Wallet Composition Over Time for Affiliate {affiliate_id_to_plot}")
        plt.legend()
        plt.show()

affiliate_earnings = analyze_results(token_histories, affiliate_histories)
plot_token_simulation(token_histories)
plot_affiliate_simulation(affiliate_histories, affiliates)

# Assuming your data is in pandas DataFrames like 'df_prices', 'df_supply', etc.

# --- Improved Token Prices Plot ---
def plot_token_prices(df_prices, title="Simulated Token Prices Over Time", event_timestamps=None):
    plt.figure(figsize=(14, 6))
    for col in df_prices.columns:
        plt.plot(df_prices.index, df_prices[col], label=col)

    if event_timestamps:
        for ts in event_timestamps:
            plt.axvline(x=ts, color='r', linestyle='--', label='Event') # Mark events

    plt.title(title)
    plt.xlabel("Simulation Step")
    plt.ylabel("Token Price")
    plt.legend()
    plt.grid(True)
    plt.show()

# Example usage:
# plot_token_prices(df_prices, event_timestamps=[500, 10000, 25000])

# --- Improved Token Supply Plot ---
def plot_token_supply(df_supply, title="Simulated Token Supply Over Time"):
    plt.figure(figsize=(14, 6))
    for col in df_supply.columns:
        plt.plot(df_supply.index, df_supply[col], label=col)
    plt.title(title)
    plt.xlabel("Simulation Step")
    plt.ylabel("Token Supply")
    plt.legend()
    plt.grid(True)
    plt.show()

# --- Improved Price vs. Supply Plot (Individual) ---
def plot_price_vs_supply_individual(df_prices, df_supply, title_prefix="Token"):
    num_tokens = len(df_prices.columns)
    fig, axes = plt.subplots(nrows=num_tokens, figsize=(10, 5 * num_tokens))

    for i, token_col in enumerate(df_prices.columns):
        axes[i].plot(df_supply[token_col], df_prices[token_col])
        axes[i].set_title(f"{title_prefix} {token_col}: Price vs. Supply")
        axes[i].set_xlabel("Supply")
        axes[i].set_ylabel("Price")
        axes[i].grid(True)

    plt.tight_layout()
    plt.show()

# plot_price_vs_supply_individual(df_prices, df_supply)

# --- Example of plotting distribution of affiliate base currency ---
def plot_affiliate_base_currency_distribution(df_affiliate_currency, time_points):
    plt.figure(figsize=(14, 6))
    for time in time_points:
        if time in df_affiliate_currency.index:
            plt.hist(df_affiliate_currency.loc[time], alpha=0.5, label=f"Step {time}")
    plt.title("Distribution of Affiliate Base Currency at Different Time Points")
    plt.xlabel("Base Currency")
    plt.ylabel("Number of Affiliates")
    plt.legend()
    plt.grid(True)
    plt.show()

# Example usage (assuming your affiliate data is structured appropriately)
# time_points_to_analyze = [1000, 5000, 10000]
# plot_affiliate_base_currency_distribution(df_affiliate_currency, time_points_to_analyze)

# --- Example of plotting stacked area chart for wallet composition ---
def plot_wallet_composition_stacked(df_wallet, title="Wallet Composition Over Time"):
    plt.figure(figsize=(14, 6))
    plt.stackplot(df_wallet.index, df_wallet.T, labels=df_wallet.columns)
    plt.title(title)
    plt.xlabel("Simulation Step")
    plt.ylabel("Token Balance")
    plt.legend(loc='upper left')
    plt.grid(True)
    plt.show()

# Example usage:
# plot_wallet_composition_stacked(df_wallet_affiliate_0)