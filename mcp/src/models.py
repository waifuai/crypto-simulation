import numpy as np
import random
import logging
from constants import INITIAL_CTX_BALANCE, NUM_RESOURCES, BASE_RESOURCE_COST, RESOURCE_CAPACITY, PRICE_ELASTICITY, MAX_RESOURCE_CAPACITY, RESOURCE_REGEN_RATE, DYNAMIC_REGEN_MULTIPLIER, RESOURCE_CAPACITY_MULTIPLIER, BANKRUPTCY_THRESHOLD, AGENT_INCOME, DYNAMIC_INCOME_MULTIPLIER, AGENT_INCOME_CEILING, AGENT_EXPENSE_RATE, MIN_AGENT_BALANCE

class Agent:
    def __init__(self, agent_id):
        self.agent_id = agent_id
        self.ctx_balance = INITIAL_CTX_BALANCE
        self.resource_demand_preference = np.random.uniform(size=NUM_RESOURCES).astype(np.float32)
        self.demand_multiplier = 0.1
        self.is_bankrupt = False
        logging.debug(f"Agent {self.agent_id} created with initial balance {self.ctx_balance} and resource needs {self.resource_demand_preference}")

    def request_resources(self, resource_prices, resource_availability):
        if self.is_bankrupt:
            return []
        requests = []
        for i in range(NUM_RESOURCES):
            demand = self.resource_demand_preference[i] * (1.0 - resource_prices[i] / (BASE_RESOURCE_COST * 5)) * self.demand_multiplier
            demand = np.clip(demand, 0.0, resource_availability[i])
            if self.ctx_balance >= resource_prices[i] * demand and self.ctx_balance > MIN_AGENT_BALANCE:
                requests.append((i, demand))
        return requests

    def adjust_needs(self):
        change = np.random.uniform(size=NUM_RESOURCES, low=-0.1, high=0.1).astype(np.float32)
        self.resource_demand_preference = np.clip(self.resource_demand_preference + change, 0.0, 1.0)

    def adjust_demand_multiplier(self, step_num):
        pass

    def add_income(self, avg_resource_price):
        income = min(AGENT_INCOME + DYNAMIC_INCOME_MULTIPLIER * avg_resource_price, AGENT_INCOME_CEILING)
        self.ctx_balance += income

    def add_expense(self):
        self.ctx_balance -= AGENT_EXPENSE_RATE * (1 + random.uniform(-0.2, 0.2))

    def tax(self, tax_amount):
        self.ctx_balance -= tax_amount

    def check_bankrupt(self):
        if self.ctx_balance <= BANKRUPTCY_THRESHOLD and not self.is_bankrupt:
            self.is_bankrupt = True
            logging.debug(f"Agent {self.agent_id} is bankrupt.")
        return self.is_bankrupt

class Resource:
    def __init__(self, resource_id):
        self.resource_id = resource_id
        self.capacity = RESOURCE_CAPACITY
        self.current_load = 0.0
        self.price = BASE_RESOURCE_COST
        logging.debug(f"Resource {self.resource_id} created with capacity {self.capacity} and price {self.price}")

    def update_price(self):
        demand_ratio = self.current_load / self.capacity
        self.price = BASE_RESOURCE_COST * (1 + demand_ratio * PRICE_ELASTICITY)

    def allocate(self, amount):
        allocated = min(amount, self.capacity - self.current_load)
        self.current_load += allocated
        return allocated

    def deallocate(self, amount):
        self.current_load -= min(amount, self.current_load)

    def regenerate(self, avg_agent_balance):
         self.capacity = min(MAX_RESOURCE_CAPACITY, self.capacity * (1 + RESOURCE_REGEN_RATE + DYNAMIC_REGEN_MULTIPLIER * avg_agent_balance))

    def adjust_capacity(self, total_economic_output):
        self.capacity = min(MAX_RESOURCE_CAPACITY, self.capacity * (1 + RESOURCE_CAPACITY_MULTIPLIER * total_economic_output))