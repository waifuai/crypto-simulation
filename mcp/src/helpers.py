import numpy as np
import random
from constants import DEALLOCATION_RATE, TAX_RATE
from models import Agent

def update_resource_prices(resources):
    for resource in resources:
        resource.update_price()

def get_resource_prices(resources):
    return np.array([r.price for r in resources])

def get_resource_availability(resources):
    return np.array([r.capacity - r.current_load for r in resources])

def get_agent_requests(agents, resource_prices, resource_availability):
    active_agents = [agent for agent in agents if not agent.is_bankrupt]
    all_requests = []
    for agent in active_agents:
        agent_requests = agent.request_resources(resource_prices, resource_availability)
        all_requests.extend([(agent, resource_id, amount) for resource_id, amount in agent_requests])
    random.shuffle(all_requests)
    return all_requests

def allocate_resources(resources, requests):
    for agent, resource_id, amount in requests:
        resource = resources[resource_id]
        allocated = resource.allocate(amount)
        cost = allocated * resource.price
        if agent.ctx_balance >= cost:
            agent.ctx_balance -= cost

def deallocate_resources(resources):
    for resource in resources:
        deallocate_amount = resource.current_load * DEALLOCATION_RATE
        resource.deallocate(deallocate_amount)

def regenerate_resources(resources, avg_agent_balance):
    for resource in resources:
        resource.regenerate(avg_agent_balance)

def adjust_agent_needs(agents):
    for agent in agents:
        agent.adjust_needs()

def adjust_agent_demand_multiplier(agents, step_num):
    for agent in agents:
        agent.adjust_demand_multiplier(step_num)

def add_agent_income(agents, avg_resource_price):
    for agent in agents:
        agent.add_income(avg_resource_price)

def add_agent_expense(agents):
    for agent in agents:
        agent.add_expense()

def check_agent_bankruptcies(agents):
    bankrupt_agents = []
    for agent in agents:
        if agent.check_bankrupt():
            bankrupt_agents.append(agent)
    return bankrupt_agents

def tax_agents(agents, tax_rate, resources):
    total_taxes = 0
    for agent in agents:
        tax_amount = agent.ctx_balance * tax_rate
        agent.tax(tax_amount)
        total_taxes += tax_amount
    return total_taxes

def redistribute_wealth(agents, total_taxes, resources):
    active_agents = [agent for agent in agents if not agent.is_bankrupt]
    if len(active_agents) > 0:
        redistribution_per_agent = total_taxes / len(active_agents)
        for agent in active_agents:
            agent.ctx_balance += redistribution_per_agent

def adjust_resource_capacity(resources, total_economic_output):
    for resource in resources:
      resource.adjust_capacity(total_economic_output)

def get_agent_balances(agents):
    return [agent.ctx_balance for agent in agents]

def get_resource_load_and_prices(resources):
    return [r.price for r in resources], [r.current_load for r in resources]

def get_total_economic_output(agents, resources):
    total_balances = sum(get_agent_balances(agents))
    resource_prices = get_resource_prices(resources)
    resource_load, _ = get_resource_load_and_prices(resources)
    total_resource_value = sum(resource_prices * resource_load)
    return total_balances + total_resource_value

def calculate_gini_coefficient(balances):
    balances = sorted(balances)
    n = len(balances)
    if n < 2:
        return 0.0
    numerator = sum((i + 1) * balance for i, balance in enumerate(balances)) - sum((n - i) * balance for i, balance in enumerate(balances))
    denominator = n * sum(balances)
    return numerator / denominator if denominator else 0.0