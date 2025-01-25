import numpy as np
import time
import random
import logging
import matplotlib.pyplot as plt

# --- Constants ---
NUM_AGENTS = 50
NUM_RESOURCES = 3
SIMULATION_STEPS = 10000
INITIAL_CTX_BALANCE = 100
RESOURCE_CAPACITY = 500
BASE_RESOURCE_COST = 1
PRICE_ELASTICITY = 0.05
DEALLOCATION_RATE = 0.05
AGENT_INCOME = 0.5
RESOURCE_REGEN_RATE = 0.01
MAX_RESOURCE_CAPACITY = 1000
AGENT_EXPENSE_RATE = 0.2
MIN_AGENT_BALANCE = 10
BANKRUPTCY_THRESHOLD = -50
DYNAMIC_INCOME_MULTIPLIER = 0.1
DYNAMIC_REGEN_MULTIPLIER = 0.001
AGENT_INCOME_CEILING = 1.0
TAX_RATE = 0.02
RESOURCE_CAPACITY_MULTIPLIER = 0.005
INITIAL_IMBALANCE = True
IMBALANCE_STRENGTH = 0.5

# --- Logging Configuration ---
logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Model Definition ---
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
        self.demand_multiplier = min(1.0, self.demand_multiplier + (0.9 / SIMULATION_STEPS))

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

# --- Helper Functions ---
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

# --- Simulation Step ---
def simulation_step(agents, resources, step_num):
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
    redistribute_wealth(agents, total_taxes, resources)
    bankrupt_agents = check_agent_bankruptcies(agents)
    agents[:] = [agent for agent in agents if agent not in bankrupt_agents]
    resource_prices_debug, resource_loads_debug = get_resource_load_and_prices(resources)
    return resource_prices, get_agent_balances(agents), resource_prices_debug, resource_loads_debug

def run_simulation(params):
    global PRICE_ELASTICITY, RESOURCE_REGEN_RATE, TAX_RATE, INITIAL_IMBALANCE, IMBALANCE_STRENGTH, SIMULATION_STEPS, NUM_AGENTS, AGENT_EXPENSE_RATE
    original_price_elasticity = PRICE_ELASTICITY
    original_resource_regen_rate = RESOURCE_REGEN_RATE
    original_tax_rate = TAX_RATE
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
    RESOURCE_REGEN_RATE = resource_regen_rate
    TAX_RATE = tax_rate
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
        resource_prices, agent_balances, _, _ = simulation_step(agents_list, resources_list, step)
        agent_balances_history.append(agent_balances)
        resource_prices_history.append(resource_prices)

    final_balances = get_agent_balances(agents_list)
    avg_final_balance = np.mean(final_balances)
    gini_coefficient = calculate_gini_coefficient(final_balances)
    num_bankruptcies = original_num_agents - len(agents_list)
    avg_final_resource_price = np.mean(resource_prices_history[-1]) if resource_prices_history else np.nan

    PRICE_ELASTICITY = original_price_elasticity
    RESOURCE_REGEN_RATE = original_resource_regen_rate
    TAX_RATE = original_tax_rate
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

# --- Parameter Experimentation ---
logging.info("Starting parameter experimentation...")

param_ranges = {
    'price_elasticity': np.linspace(0.01, 0.1, 10),
    'resource_regen_rate': np.linspace(0.005, 0.02, 10),
    'tax_rate': np.linspace(0.0, 0.05, 10),
    'agent_expense_rate': np.linspace(0.1, 0.5, 10)
}

experiment_results = {}

for param_name, param_values in param_ranges.items():
    logging.info(f"Experimenting with {param_name}...")
    experiment_results[param_name] = []
    for value in param_values:
        params = {param_name: value}
        logging.info(f"Running simulation with {param_name} = {value}")
        results = run_simulation(params)
        results['param_value'] = value
        experiment_results[param_name].append(results)

# --- Visualize Results ---
logging.info("Visualizing results...")
plt.figure(figsize=(18, 15))
plot_index = 1

for param_name in param_ranges.keys():
    param_values = [res['param_value'] for res in experiment_results[param_name]]

    plt.subplot(len(param_ranges), 4, plot_index)
    avg_balances = [res['avg_final_balance'] for res in experiment_results[param_name]]
    plt.plot(param_values, avg_balances)
    plt.title(f"Avg Final Balance vs {param_name}")
    plt.xlabel(param_name)
    plt.ylabel("Average Final Balance")
    plot_index += 1

    plt.subplot(len(param_ranges), 4, plot_index)
    gini_coeffs = [res['gini_coefficient'] for res in experiment_results[param_name]]
    plt.plot(param_values, gini_coeffs)
    plt.title(f"Gini Coefficient vs {param_name}")
    plt.xlabel(param_name)
    plt.ylabel("Gini Coefficient")
    plot_index += 1

    plt.subplot(len(param_ranges), 4, plot_index)
    bankruptcies = [res['num_bankruptcies'] for res in experiment_results[param_name]]
    plt.plot(param_values, bankruptcies)
    plt.title(f"Number of Bankruptcies vs {param_name}")
    plt.xlabel(param_name)
    plt.ylabel("Number of Bankruptcies")
    plot_index += 1

    plt.subplot(len(param_ranges), 4, plot_index)
    avg_resource_prices = [res['avg_final_resource_price'] for res in experiment_results[param_name]]
    plt.plot(param_values, avg_resource_prices)
    plt.title(f"Avg Final Resource Price vs {param_name}")
    plt.xlabel(param_name)
    plt.ylabel("Average Final Resource Price")
    plot_index += 1

plt.tight_layout()
plt.savefig("parameter_impact.png")
logging.info("Parameter impact plots saved to parameter_impact.png")

# --- Further Analysis (Example) ---
logging.info("Performing further analysis...")

if 'tax_rate' in experiment_results:
    tax_results = experiment_results['tax_rate']
    best_tax_rate_data = min(tax_results, key=lambda x: x['num_bankruptcies'])
    logging.info(f"Tax rate that minimizes bankruptcies: {best_tax_rate_data['param_value']}")

if 'resource_regen_rate' in experiment_results:
    regen_results = experiment_results['resource_regen_rate']
    best_regen_rate_data = max(regen_results, key=lambda x: x['avg_final_balance'])
    logging.info(f"Regen rate that maximizes average final balance: {best_regen_rate_data['param_value']}")

logging.info("Experimentation and analysis complete.")