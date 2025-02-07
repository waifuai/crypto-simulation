import time
import logging
import numpy as np
from constants import bonding_curve_change_intervals, BONDING_CURVE_PARAM_CHANGE_INTERVAL, INITIAL_TOKEN_INVESTMENT
from bonding_curves import bonding_curve_functions
from crypto_token import Token
from affiliate import Affiliate
from config import NUM_SIMULATION_STEPS, NUM_TOKENS, NUM_AFFILIATES, INITIAL_SUPPLY, INITIAL_PRICE, INITIAL_COMMISSION_RATE
from typing import Dict, Any, Tuple, List

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

tokens: List[Token] = [
    Token(
        f"Token_{i}",
        INITIAL_SUPPLY,
        INITIAL_PRICE,
        bonding_curve_functions[np.random.choice(len(bonding_curve_functions))],
    )
    for i in range(NUM_TOKENS)
]

affiliates: List[Affiliate] = [Affiliate(i, INITIAL_COMMISSION_RATE, i < (NUM_AFFILIATES // 5)) for i in range(NUM_AFFILIATES)]

def token_simulation_step(step: int) -> None:
    """
    Simulates a single step of the token economy.

    Args:
        step (int): The current step in the simulation.
    """
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

            token_price = token.price
            if token_price > 0: # Avoid division by zero
                tokens_to_trade = invest_amount / token_price
            else:
                tokens_to_trade = 0
                continue # Skip if price is zero

            if np.random.rand() < 0.6:  # Slightly adjusted probability for buy
                cost = tokens_to_trade * token_price
                if affiliate.base_currency_balance >= cost:
                    token.buy(np.array(tokens_to_trade, dtype=np.float32))
                    affiliate.base_currency_balance -= np.array(cost, dtype=np.float32)
                    if token.name not in affiliate.wallet:
                        affiliate.wallet[token.name] = np.array(0.0, dtype=np.float32)
                    affiliate.wallet[token.name] += np.array(tokens_to_trade, dtype=np.float32)
                    logging.debug(f"Affiliate {affiliate.affiliate_id} bought {tokens_to_trade:.2f} {token.name} for {cost:.2f}")
                    affiliate.track_referral(cost) # Track commission on buy
                else:
                    logging.debug(f"Affiliate {affiliate.affiliate_id} could not afford to buy {token.name}")
            else:
                tokens_available = affiliate.wallet.get(token.name, 0)
                tokens_to_sell = min(tokens_to_trade, tokens_available)
                if tokens_to_sell > 0:
                    sale_proceeds = token.sell(np.array(tokens_to_sell, dtype=np.float32)) * tokens_to_sell
                    affiliate.wallet[token.name] -= np.array(tokens_to_sell, dtype=np.float32)
                    affiliate.base_currency_balance += np.array(sale_proceeds, dtype=np.float32)
                    logging.debug(f"Affiliate {affiliate.affiliate_id} sold {tokens_to_sell:.2f} {token.name} for {sale_proceeds:.2f}")
                    affiliate.track_referral(sale_proceeds) # Track commission on sell
                else:
                    logging.debug(f"Affiliate {affiliate.affiliate_id} has no {token.name} to sell")

            affiliate.recent_investment.append(invest_amount)
            if len(affiliate.recent_investment) > 50: # MOVING_AVERAGE_WINDOW:
                affiliate.recent_investment.pop(0)

    for i, token in enumerate(tokens):
        if step % bonding_curve_change_intervals[i] == 0:
            token.change_bonding_curve()

        if step % BONDING_CURVE_PARAM_CHANGE_INTERVAL == 0: # More frequent parameter changes
            token.change_bonding_curve_parameters()

    logging.debug(f"Finished token simulation step: {step}")

def affiliate_simulation_step(step: int) -> None:
    """
    Simulates a single step of the affiliate behavior.

    Args:
        step (int): The current step in the simulation.
    """
    logging.debug(f"Starting affiliate simulation step: {step}")
    for affiliate in affiliates:
        for token_name in list(affiliate.wallet.keys()):
            if affiliate.wallet[token_name] > 0 and np.random.rand() < 0.05: # Reduced sell frequency
                tokens_to_sell_percentage = np.random.rand() * 0.05 # Sell up to 5%
                tokens_to_sell = affiliate.wallet[token_name] * tokens_to_sell_percentage

                for token in tokens:
                    if token.name == token_name:
                        sale_proceeds = token.sell(np.array(tokens_to_sell, dtype=np.float32)) * token.price
                        affiliate.wallet[token_name] -= np.array(tokens_to_sell, dtype=np.float32)
                        affiliate.base_currency_balance += np.array(sale_proceeds, dtype=np.float32)
                        logging.debug(f"Affiliate {affiliate.affiliate_id} sold {tokens_to_sell:.2f} {token.name} for {sale_proceeds:.2f} (periodic sell)")
                        affiliate.track_referral(sale_proceeds) # Track commission on periodic sell
                        break

        affiliate.earnings_history.append(affiliate.total_earned)
        affiliate.commission_rate_history.append(
            affiliate.commission_rate
        )
        affiliate.adjust_commission_dynamically(step)

    logging.debug(f"Finished affiliate simulation step: {step}")

def run_simulation() -> Tuple[Dict[str, Dict[str, List[Any]]], Dict[int, Dict[str, List[Any]]]]:
    """
    Runs the entire simulation.

    Returns:
        Tuple[Dict[str, Dict[str, List[Any]]], Dict[int, Dict[str, List[Any]]]]: A tuple containing the token histories and affiliate histories.
    """
    token_histories: Dict[str, Dict[str, List[Any]]] = {
        token.name: {
            "price": [],
            "supply": [],
            "bonding_curve": [],
        }
        for token in tokens
    }
    affiliate_histories: Dict[int, Dict[str, List[Any]]] = {
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
            token_histories[token.name]["price"].append(token.price)
            token_histories[token.name]["supply"].append(token.supply)
            token_histories[token.name]["bonding_curve"].append(
                token.bonding_curve_func.__name__
            )

        for affiliate in affiliates:
            affiliate_histories[affiliate.affiliate_id]["earned"].append(
                affiliate.total_earned
            )
            affiliate_histories[affiliate.affiliate_id][
                "commission_rate"
            ].append(affiliate.commission_rate)
            affiliate_histories[affiliate.affiliate_id]["wallet"].append(
                {
                    token_name: wallet_balance
                    for token_name, wallet_balance in affiliate.wallet.items()
                }
            )
            affiliate_histories[affiliate.affiliate_id]["base_currency_balance"].append(
                affiliate.base_currency_balance
            )

    end_time = time.time()
    logging.info(f"Simulation Completed in: {end_time - start_time:.2f} seconds")
    return token_histories, affiliate_histories