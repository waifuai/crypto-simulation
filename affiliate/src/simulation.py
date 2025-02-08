import time
import logging
import numpy as np
from typing import Dict, Any, Tuple, List

from affiliate.src.config import NUM_SIMULATION_STEPS, NUM_TOKENS, NUM_AFFILIATES, INITIAL_SUPPLY, INITIAL_PRICE, INITIAL_COMMISSION_RATE, BONDING_CURVE_PARAM_CHANGE_INTERVAL
from affiliate.src.config import bonding_curve_change_intervals
from affiliate.src.bonding_curves import bonding_curve_functions
from affiliate.src.crypto_token import Token
from affiliate.src.affiliate import Affiliate

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

def _process_affiliate_trades(affiliate: Affiliate, tokens: List[Token], step: int, params: Dict[str, Any]) -> Affiliate:
    """Processes the trades for a single affiliate."""
    num_transactions = np.random.randint(1, 3) if not affiliate.is_whale else np.random.randint(0, 2)
    initial_token_investment = params.get('initial_token_investment', 10)

    for _ in range(num_transactions):
        random_token_index = np.random.randint(len(tokens))
        token = tokens[random_token_index]

        if affiliate.is_whale and affiliate.whale_investment_capacity > 0:
            invest_amount = affiliate.whale_investment_capacity * np.random.uniform(0.1, 0.4)
        else:
            invest_amount = initial_token_investment + (np.random.rand(1)[0] * 5)

        token_price = token.price
        if token_price > 0:
            tokens_to_trade = invest_amount / token_price
        else:
            tokens_to_trade = 0
            continue

        if np.random.rand() < 0.6:  # Slightly adjusted probability for buy
            cost = tokens_to_trade * token_price
            if affiliate.base_currency_balance >= cost:
                token = _buy_token(token, affiliate, tokens_to_trade, cost)
                logging.debug(f"Affiliate {affiliate.affiliate_id} bought {tokens_to_trade:.2f} {token.name} for {cost:.2f}")
            else:
                logging.debug(f"Affiliate {affiliate.affiliate_id} could not afford to buy {token.name}")
        else:
            affiliate = _sell_token(token, affiliate, tokens_to_trade)

        affiliate.recent_investment.append(invest_amount)
        if len(affiliate.recent_investment) > 50:  # MOVING_AVERAGE_WINDOW:
            affiliate.recent_investment.pop(0)
    return affiliate

def _buy_token(token: Token, affiliate: Affiliate, tokens_to_trade: float, cost: float) -> Token:
    """Executes a buy order."""
    token.buy(np.array(tokens_to_trade, dtype=np.float32))
    affiliate.base_currency_balance -= np.array(cost, dtype=np.float32)
    if token.name not in affiliate.wallet:
        affiliate.wallet[token.name] = np.array(0.0, dtype=np.float32)
    affiliate.wallet[token.name] += np.array(tokens_to_trade, dtype=np.float32)
    affiliate.track_referral(cost)  # Track commission on buy
    return token

def _sell_token(token: Token, affiliate: Affiliate, tokens_to_trade: float) -> Affiliate:
    """Executes a sell order."""
    tokens_available = affiliate.wallet.get(token.name, 0)
    tokens_to_sell = min(tokens_to_trade, tokens_available)
    if tokens_to_sell > 0:
        sale_proceeds = token.sell(np.array(tokens_to_sell, dtype=np.float32)) * tokens_to_sell
        affiliate.wallet[token.name] -= np.array(tokens_to_sell, dtype=np.float32)
        affiliate.base_currency_balance += np.array(sale_proceeds, dtype=np.float32)
        logging.debug(f"Affiliate {affiliate.affiliate_id} sold {tokens_to_sell:.2f} {token.name} for {sale_proceeds:.2f}")
        affiliate.track_referral(sale_proceeds)  # Track commission on sell
    else:
        logging.debug(f"Affiliate {affiliate.affiliate_id} has no {token.name} to sell")
    return affiliate

def _update_tokens(tokens: List[Token], step: int, params: Dict[str, Any]) -> List[Token]:
    """Updates the bonding curve of each token."""
    bonding_curve_param_change_interval = params.get('bonding_curve_param_change_interval', 20)
    for i, token in enumerate(tokens):
        if step % bonding_curve_change_intervals[i] == 0:
            token.change_bonding_curve()

        if step % bonding_curve_param_change_interval == 0:  # More frequent parameter changes
            token.change_bonding_curve_parameters()
    return tokens

def token_simulation_step(step: int, tokens: List[Token], affiliates: List[Affiliate], params: Dict[str, Any]) -> None:
    """
    Simulates a single step of the token economy.

    Args:
        step (int): The current step in the simulation.
        tokens (List[Token]): The list of tokens in the simulation.
        affiliates (List[Affiliate]): The list of affiliates in the simulation.
        params (Dict[str, Any]): Dictionary of simulation parameters.
    """
    logging.debug(f"Starting token simulation step: {step}")
    for affiliate in affiliates:
        affiliate = _process_affiliate_trades(affiliate, tokens, step, params)

    tokens = _update_tokens(tokens, step, params)

    logging.debug(f"Finished token simulation step: {step}")

def affiliate_simulation_step(step: int, tokens: List[Token], affiliates: List[Affiliate], params: Dict[str, Any]) -> None:
    """
    Simulates a single step of the affiliate behavior.

    Args:
        step (int): The current step in the simulation.
        tokens (List[Token]): The list of tokens in the simulation.
        affiliates (List[Affiliate]): The list of affiliates in the simulation.
        params (Dict[str, Any]): Dictionary of simulation parameters.
    """
    logging.debug(f"Starting affiliate simulation step: {step}")
    for affiliate in affiliates:
        for token_name in list(affiliate.wallet.keys()):
            if affiliate.wallet[token_name] > 0 and np.random.rand() < 0.05:  # Reduced sell frequency
                tokens_to_sell_percentage = np.random.rand() * 0.05  # Sell up to 5%
                tokens_to_sell = affiliate.wallet[token_name] * tokens_to_sell_percentage

                for token in tokens:
                    if token.name == token_name:
                        sale_proceeds = token.sell(np.array(tokens_to_sell, dtype=np.float32)) * token.price
                        affiliate.wallet[token_name] -= np.array(tokens_to_sell, dtype=np.float32)
                        affiliate.base_currency_balance += np.array(sale_proceeds, dtype=np.float32)
                        logging.debug(f"Affiliate {affiliate.affiliate_id} sold {tokens_to_sell:.2f} {token.name} for {sale_proceeds:.2f} (periodic sell)")
                        affiliate.track_referral(sale_proceeds)  # Track commission on periodic sell
                        break

        affiliate.earnings_history.append(affiliate.total_earned)
        affiliate.commission_rate_history.append(
            affiliate.commission_rate
        )
        affiliate.adjust_commission_dynamically(step)

    logging.debug(f"Finished affiliate simulation step: {step}")

def run_simulation(params: Dict[str, Any]) -> Tuple[Dict[str, Dict[str, List[Any]]], Dict[int, Dict[str, List[Any]]]]:
    """
    Runs the entire simulation.

    Args:
        params (Dict[str, Any]): A dictionary of simulation parameters.

    Returns:
        Tuple[Dict[str, Dict[str, List[Any]]], Dict[int, Dict[str, List[Any]]]]: A tuple containing the token histories and affiliate histories.
    """
    initial_supply = params.get('initial_supply', 10000)
    initial_price = params.get('initial_price', 1.0)
    num_tokens = params.get('num_tokens', 5)
    num_affiliates = params.get('num_affiliates', 5)
    bonding_curve_functions_list = params.get('bonding_curve_functions', bonding_curve_functions)

    tokens: List[Token] = [
        Token(
            f"Token_{i}",
            initial_supply,
            initial_price,
            bonding_curve_functions_list[np.random.choice(len(bonding_curve_functions_list))],
        )
        for i in range(num_tokens)
    ]

    initial_commission_rate = params.get('initial_commission_rate', 0.10)
    affiliates: List[Affiliate] = [Affiliate(i, initial_commission_rate, i < (num_affiliates // 5)) for i in range(num_affiliates)]

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
    num_simulation_steps = params.get('num_simulation_steps', 100)
    for step in range(num_simulation_steps):
        token_simulation_step(step, tokens, affiliates, params)
        affiliate_simulation_step(step, tokens, affiliates, params)

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