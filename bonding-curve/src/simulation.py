import numpy as np
from config import INITIAL_TOKEN_SUPPLY, NUM_AGENTS, TRADING_FEE
from bonding_curves import calculate_bonding_curve_price
from agent import Agent
from typing import List, Tuple, Dict, Any

# --- Simulation State Class ---
class SimulationState:
    """
    Represents the global state of the simulation.
    """
    def __init__(self):
        self.supply: float = INITIAL_TOKEN_SUPPLY
        self.agents: List[Agent] = [Agent(i) for i in range(NUM_AGENTS)]

global_state = SimulationState()

# --- Simulation Step ---
def simulation_step(current_step: int, bonding_curve_params: Dict[str, Any]) -> Tuple[float, List[float], List[float], float]:
    """
    Simulates a single step in the bonding curve simulation.

    Args:
        current_step (int): The current simulation step.
        bonding_curve_params (Dict[str, Any]): The parameters of the bonding curve.

    Returns:
        Tuple[float, List[float], List[float], float]: A tuple containing the current supply, agent capitals, agent tokens, and current price.
    """
    global global_state
    trades = []
    current_price = calculate_bonding_curve_price(global_state.supply, bonding_curve_params)

    # Track price movement
    price_changes = []
    previous_price = current_price

    for agent in global_state.agents:
        agent.update_memory(current_price)

    for agent in global_state.agents:
        trade_type, trade_amount = agent.trade(global_state.supply, current_step, bonding_curve_params)
        if trade_type is not None:
            trades.append((agent, trade_type, trade_amount))

    for agent, trade_type, trade_amount in trades:
        if trade_type == "buy":
            price = calculate_bonding_curve_price(global_state.supply, bonding_curve_params) * (1 + TRADING_FEE)
            cost = trade_amount * price
            if agent.capital >= cost:
                if agent.capital >= cost:
                    agent.capital -= cost
                    agent.tokens += trade_amount
                    global_state.supply += trade_amount

        elif trade_type == "sell":
            price = calculate_bonding_curve_price(global_state.supply, bonding_curve_params) * (1 - TRADING_FEE)
            revenue = trade_amount * price
            agent.capital += revenue
            agent.tokens -= trade_amount
            global_state.supply -= trade_amount

    # Calculate price impact
    if len(trades) > 0:
        new_price = calculate_bonding_curve_price(global_state.supply, bonding_curve_params)
        price_changes.append(abs(new_price - previous_price))

    return global_state.supply, [agent.capital for agent in global_state.agents], [
        agent.tokens for agent in global_state.agents
    ], current_price