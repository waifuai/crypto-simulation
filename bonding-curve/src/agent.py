import numpy as np
import random
from config import INITIAL_AGENT_CAPITAL, AGENT_MEMORY_SIZE, AGENT_TREND_THRESHOLD, AGENT_TREND_DELAY, AGENT_TRADE_FREQUENCY, AGENT_TRADE_SIZE_RANGE, TRADING_FEE, INITIAL_TOKEN_PRICE
from bonding_curves import calculate_bonding_curve_price

# --- Agent State ---
class Agent:
    def __init__(self, agent_id):
        self.agent_id = agent_id
        self.capital = INITIAL_AGENT_CAPITAL
        self.tokens = 0.0
        # Initialize with first price instead of zeros
        self.price_memory = np.full(AGENT_MEMORY_SIZE, INITIAL_TOKEN_PRICE)
        self.last_trade_step = -AGENT_TREND_DELAY

    def update_memory(self, current_price):
        if current_price is not None:
            self.price_memory = np.concatenate((self.price_memory[1:], [current_price]))

    def trade(self, current_supply, current_step, bonding_curve_params):
        if random.random() < AGENT_TRADE_FREQUENCY and current_step > (self.last_trade_step + AGENT_TREND_DELAY):
            trade_size = random.uniform(
                AGENT_TRADE_SIZE_RANGE[0], AGENT_TRADE_SIZE_RANGE[1]
            )

            current_price = calculate_bonding_curve_price(current_supply, bonding_curve_params)

            if np.sum(self.price_memory) != 0.0:
                average_price = np.mean(self.price_memory[:-1])
                price_diff = (self.price_memory[-1] - average_price) / average_price
                if price_diff > AGENT_TREND_THRESHOLD:
                    max_buy_tokens = self.capital / (current_price * (1 + TRADING_FEE))
                    tokens_to_buy = max_buy_tokens * trade_size
                    self.last_trade_step = current_step
                    return "buy", tokens_to_buy
                elif price_diff < -AGENT_TREND_THRESHOLD and self.tokens > 0:
                    tokens_to_sell = self.tokens * trade_size
                    self.last_trade_step = current_step
                    return "sell", tokens_to_sell

            if self.capital > 0:
                max_buy_tokens = self.capital / (current_price * (1 + TRADING_FEE))
                tokens_to_buy = max_buy_tokens * trade_size
                self.last_trade_step = current_step
                return "buy", tokens_to_buy

            elif self.tokens > 0:
                tokens_to_sell = self.tokens * trade_size
                self.last_trade_step = current_step
                return "sell", tokens_to_sell

        return None, 0