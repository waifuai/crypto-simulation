import numpy as np
from constants import SIMULATION_STEPS, NUM_RESOURCES, TAX_RATE, NUM_AGENTS
from helpers import update_resource_prices, get_resource_prices, get_resource_availability, get_agent_requests, allocate_resources, deallocate_resources, regenerate_resources, adjust_agent_needs, adjust_agent_demand_multiplier, add_agent_income, add_agent_expense, check_agent_bankruptcies, tax_agents, redistribute_wealth, adjust_resource_capacity, get_agent_balances, get_total_economic_output, calculate_gini_coefficient, get_resource_load_and_prices
from models import Agent, Resource
from typing import List, Dict, Any

def simulation_step(agents: List[Agent], resources: List[Resource], step_num: int) -> Dict[str, Any]:
    """
    Runs a single step of the simulation.

    Args:
        agents (List[Agent]): List of agents.
        resources (List[Resource]): List of resources.
        step_num (int): The current step number.

    Returns:
        Dict[str, Any]: A dictionary containing metrics for the current step.
    """
    update_resource_prices(resources)
    resource_prices = get_resource_prices(resources)
    resource_availability = get_resource_availability(resources)
    avg_resource_price = np.mean(resource_prices)
    avg_agent_balance = np.mean(get_agent_balances(agents))
    all_requests = get_agent_requests(agents, resource_prices, resource_availability)
    allocate_resources(resources, all_requests)
    deallocate_resources(resources)
    regenerate_resources(resources, avg_agent_balance)
    total_economic_output = get_total_economic_output(agents, resources)
    adjust_resource_capacity(resources, total_economic_output)
    adjust_agent_needs(agents)
    adjust_agent_demand_multiplier(agents, step_num)
    add_agent_income(agents, avg_resource_price)
    add_agent_expense(agents)
    total_taxes = tax_agents(agents, TAX_RATE, resources)
    total_taxes_redistributed = redistribute_wealth(agents, total_taxes, resources)
    bankrupt_agents = check_agent_bankruptcies(agents)
    agents[:] = [agent for agent in agents if agent not in bankrupt_agents]
    resource_prices_debug, resource_loads_debug = get_resource_load_and_prices(resources)
    current_gini = calculate_gini_coefficient(get_agent_balances(agents))
    agent_balances = get_agent_balances(agents)
    return {
        "step": step_num,
        "gini": current_gini,
        "median_balance": np.median(agent_balances),
        "resource_utilization": [r.current_load/r.capacity for r in resources],
        "price_variance": np.var(resource_prices),
        "bankruptcy_rate": len(bankrupt_agents)/NUM_AGENTS,
        "tax_redistribution": total_taxes_redistributed,
        "economic_output": total_economic_output
    }

def run_simulation(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Runs the simulation with the given parameters.

    Args:
        params (Dict[str, Any]): A dictionary of parameters to override the default constants.

    Returns:
        Dict[str, Any]: A dictionary containing the results of the simulation.
    """
    from constants import PRICE_ELASTICITY, RESOURCE_REGEN_RATE, INITIAL_IMBALANCE, IMBALANCE_STRENGTH, SIMULATION_STEPS, NUM_AGENTS, AGENT_EXPENSE_RATE
    original_price_elasticity = PRICE_ELASTICITY
    original_resource_regen_rate = RESOURCE_REGEN_RATE
    original_initial_imbalance = INITIAL_IMBALANCE
    original_imbalance_strength = IMBALANCE_STRENGTH
    original_simulation_steps = SIMULATION_STEPS
    original_num_agents = NUM_AGENTS
    original_agent_expense_rate = AGENT_EXPENSE_RATE

    num_agents = params.get('num_agents', NUM_AGENTS)
    simulation_steps = params.get('simulation_steps', SIMULATION_STEPS)
    price_elasticity = params.get('price_elasticity', PRICE_ELASTICITY)
    resource_regen_rate = params.get('resource_regen_rate', RESOURCE_REGEN_RATE)
    tax_rate = params.get('tax_rate', TAX_RATE)
    initial_imbalance = params.get('initial_imbalance', INITIAL_IMBALANCE)
    imbalance_strength = params.get('imbalance_strength', IMBALANCE_STRENGTH)
    agent_expense_rate = params.get('agent_expense_rate', AGENT_EXPENSE_RATE)

    PRICE_ELASTICITY = price_elasticity
    PRICE_ELASTICITY = price_elasticity
    RESOURCE_REGEN_RATE = resource_regen_rate
    INITIAL_IMBALANCE = initial_imbalance
    IMBALANCE_STRENGTH = imbalance_strength
    SIMULATION_STEPS = simulation_steps
    NUM_AGENTS = num_agents
    AGENT_EXPENSE_RATE = agent_expense_rate
    agents_list = [Agent(i) for i in range(num_agents)]
    resources_list = [Resource(i) for i in range(NUM_RESOURCES)]

    if INITIAL_IMBALANCE:
        for agent in agents_list:
            if agent.agent_id < NUM_AGENTS * IMBALANCE_STRENGTH:
                agent.ctx_balance *= 2
            else:
                agent.ctx_balance *= 0.5

    agent_balances_history = []
    resource_prices_history = []

    for step in range(SIMULATION_STEPS):
        step_metrics = simulation_step(agents_list, resources_list, step) # Modified line: capture metrics
        agent_balances_history.append(get_agent_balances(agents_list)) # Still append agent balances history
        resource_prices_history.append(get_resource_prices(resources_list)) # Still append resource prices history

    final_balances = get_agent_balances(agents_list)
    avg_final_balance = np.mean(final_balances)
    gini_coefficient = calculate_gini_coefficient(final_balances)
    num_bankruptcies = original_num_agents - len(agents_list)
    avg_final_resource_price = np.mean(resource_prices_history[-1]) if resource_prices_history else np.nan

    PRICE_ELASTICITY = original_price_elasticity
    RESOURCE_REGEN_RATE = original_resource_regen_rate
    INITIAL_IMBALANCE = original_initial_imbalance
    IMBALANCE_STRENGTH = original_imbalance_strength
    SIMULATION_STEPS = original_simulation_steps
    NUM_AGENTS = original_num_agents
    AGENT_EXPENSE_RATE = original_agent_expense_rate

    return {
        'avg_final_balance': avg_final_balance,
        'gini_coefficient': gini_coefficient,
        'num_bankruptcies': num_bankruptcies,
        'avg_final_resource_price': avg_final_resource_price
    }