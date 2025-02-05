import pytest
import numpy as np
import random

from simulation import run_simulation, simulation_step
from models import Agent, Resource
from helpers import (
    update_resource_prices,
    get_resource_prices,
    get_resource_availability,
    get_agent_requests,
    allocate_resources,
    deallocate_resources,
    regenerate_resources,
    adjust_agent_needs,
    adjust_agent_demand_multiplier,
    add_agent_income,
    add_agent_expense,
    check_agent_bankruptcies,
    tax_agents,
    redistribute_wealth,
    adjust_resource_capacity,
    get_agent_balances,
    get_resource_load_and_prices,
    get_total_economic_output,
    calculate_gini_coefficient
)
from constants import (
    NUM_RESOURCES,
    NUM_AGENTS,
    BASE_RESOURCE_COST,
    PRICE_ELASTICITY,
    DEALLOCATION_RATE,
    RESOURCE_CAPACITY,
    RESOURCE_REGEN_RATE,
    DYNAMIC_REGEN_MULTIPLIER,
    MAX_RESOURCE_CAPACITY,
    AGENT_INCOME,
    DYNAMIC_INCOME_MULTIPLIER,
    AGENT_INCOME_CEILING,
    AGENT_EXPENSE_RATE,
    MIN_AGENT_BALANCE,
    BANKRUPTCY_THRESHOLD,
    TAX_RATE,
    RESOURCE_CAPACITY_MULTIPLIER
)

# Ensure reproducibility across tests.
@pytest.fixture(autouse=True)
def set_seed():
    np.random.seed(42)
    random.seed(42)

# -----------------------------
# Tests for the Simulation Module
# -----------------------------
def test_run_simulation_default():
    """
    run_simulation returns a dictionary with expected keys and value types.
    """
    result = run_simulation({})
    for key in ['avg_final_balance', 'gini_coefficient', 'num_bankruptcies', 'avg_final_resource_price']:
        assert key in result, f"Missing key: {key}"
    assert isinstance(result['avg_final_balance'], float)
    assert isinstance(result['gini_coefficient'], float)
    assert isinstance(result['num_bankruptcies'], int)
    assert isinstance(result['avg_final_resource_price'], float)

def test_simulation_step_metrics():
    """
    simulation_step returns a metrics dictionary containing all required keys.
    """
    agents = [Agent(i) for i in range(10)]
    resources = [Resource(i) for i in range(NUM_RESOURCES)]
    metrics = simulation_step(agents, resources, step_num=0)
    expected_keys = [
        "step", "gini", "median_balance", "resource_utilization",
        "price_variance", "bankruptcy_rate", "tax_redistribution", "economic_output"
    ]
    for key in expected_keys:
        assert key in metrics, f"Missing key in simulation step metrics: {key}"
    assert metrics["step"] == 0
    assert isinstance(metrics["resource_utilization"], list)
    assert len(metrics["resource_utilization"]) == NUM_RESOURCES

# -----------------------------
# Tests for the Models Module (Agent and Resource)
# -----------------------------
def test_agent_requests():
    """
    Test Agent.request_resources returns a list of requests when conditions are met.
    """
    agent = Agent(0)
    # Setup: assume a single resource with fixed price and availability.
    resource_price = 1.0
    resource_avail = 100.0
    # Use a one-element list for prices and availability.
    requests = agent.request_resources([resource_price], [resource_avail])
    assert isinstance(requests, list)
    # If agent balance is high and MIN_AGENT_BALANCE condition holds,
    # we expect at least one request (if demand is non-zero).
    # It is possible that randomness yields an empty list; so we check that the structure is correct.
    if requests:
        for req in requests:
            agent_obj, res_id, amount = req
            assert isinstance(agent_obj, Agent)
            assert isinstance(res_id, int)
            assert isinstance(amount, float)

def test_resource_update_price():
    """
    Test that Resource.update_price computes the new price based on load.
    """
    resource = Resource(0)
    resource.capacity = 100.0
    resource.current_load = 50.0
    resource.price = BASE_RESOURCE_COST
    resource.update_price()
    expected_price = BASE_RESOURCE_COST * (1 + (50.0 / 100.0) * PRICE_ELASTICITY)
    assert np.isclose(resource.price, expected_price), f"Expected {expected_price}, got {resource.price}"

def test_agent_bankruptcy():
    """
    Test that an Agent becomes flagged as bankrupt when its balance is below the threshold.
    """
    agent = Agent(0)
    agent.ctx_balance = BANKRUPTCY_THRESHOLD - 1
    is_bankrupt = agent.check_bankrupt()
    assert is_bankrupt is True

def test_add_income_and_expense():
    """
    Test that adding income increases balance and adding expense decreases balance.
    """
    agent = Agent(0)
    original_balance = agent.ctx_balance
    # Test income addition
    avg_resource_price = 2.0
    add_agent_income([agent], avg_resource_price)
    expected_income = min(AGENT_INCOME + DYNAMIC_INCOME_MULTIPLIER * avg_resource_price, AGENT_INCOME_CEILING)
    assert np.isclose(agent.ctx_balance, original_balance + expected_income)
    
    # Test expense subtraction
    balance_before_expense = agent.ctx_balance
    add_agent_expense([agent])
    # Expense amount is AGENT_EXPENSE_RATE * (1 + random_factor) where random_factor ∈ [-0.2,0.2]
    expense = balance_before_expense - agent.ctx_balance
    max_expected = AGENT_EXPENSE_RATE * 1.2
    min_expected = AGENT_EXPENSE_RATE * 0.8
    assert min_expected <= expense <= max_expected

# -----------------------------
# Tests for the Helpers Module
# -----------------------------
def test_update_and_get_resource_prices():
    """
    Test that update_resource_prices updates resource prices and get_resource_prices returns them.
    """
    resources = [Resource(i) for i in range(3)]
    # Set up a custom scenario.
    for r in resources:
        r.capacity = 100.0
        r.current_load = 20.0 * (r.resource_id + 1)  # Vary current load
        r.price = BASE_RESOURCE_COST
    update_resource_prices(resources)
    prices = get_resource_prices(resources)
    for r, price in zip(resources, prices):
        expected = BASE_RESOURCE_COST * (1 + (r.current_load / r.capacity) * PRICE_ELASTICITY)
        assert np.isclose(price, expected)

def test_get_resource_availability():
    """
    Test that get_resource_availability returns the correct available capacity.
    """
    resources = [Resource(0)]
    resources[0].capacity = 100.0
    resources[0].current_load = 40.0
    availability = get_resource_availability(resources)
    np.testing.assert_allclose(availability, np.array([60.0]))

def test_allocate_resources():
    """
    Test that allocate_resources properly allocates requested resources and charges the agent.
    """
    # Create an agent with sufficient balance.
    agent = Agent(0)
    agent.ctx_balance = 1000.0
    resource = Resource(0)
    resource.capacity = 100.0
    resource.current_load = 0.0
    resource.price = 2.0
    # Create a request: agent requests 30 units of resource 0.
    requests = [(agent, 0, 30.0)]
    allocate_resources([resource], requests)
    # Resource load should increase by 30, and agent balance should decrease by 30 * 2.0.
    assert np.isclose(resource.current_load, 30.0)
    assert np.isclose(agent.ctx_balance, 1000.0 - 60.0)

def test_deallocate_resources():
    """
    Test that deallocate_resources reduces the resource's current load by DEALLOCATION_RATE.
    """
    resource = Resource(0)
    resource.capacity = 100.0
    resource.current_load = 80.0
    deallocate_resources([resource])
    expected_load = 80.0 - (80.0 * DEALLOCATION_RATE)
    assert np.isclose(resource.current_load, expected_load)

def test_regenerate_resources():
    """
    Test that regenerate_resources increases the resource capacity as expected.
    """
    resource = Resource(0)
    resource.capacity = 100.0
    avg_agent_balance = 50.0
    regenerate_resources([resource], avg_agent_balance)
    factor = 1 + RESOURCE_REGEN_RATE + DYNAMIC_REGEN_MULTIPLIER * avg_agent_balance
    expected_capacity = min(MAX_RESOURCE_CAPACITY, 100.0 * factor)
    assert np.isclose(resource.capacity, expected_capacity)

def test_adjust_agent_needs():
    """
    Test that adjust_agent_needs changes each agent's demand preferences within [0,1].
    """
    agents = [Agent(i) for i in range(5)]
    old_preferences = [agent.resource_demand_preference.copy() for agent in agents]
    adjust_agent_needs(agents)
    for agent, old_pref in zip(agents, old_preferences):
        # Check that new preferences are between 0 and 1.
        assert np.all(agent.resource_demand_preference >= 0.0)
        assert np.all(agent.resource_demand_preference <= 1.0)
        # It is possible (though unlikely) they are unchanged; so we do not enforce change.

def test_adjust_agent_demand_multiplier():
    """
    Test that adjust_agent_demand_multiplier can be called without error.
    (Currently a no-op.)
    """
    agents = [Agent(i) for i in range(5)]
    try:
        adjust_agent_demand_multiplier(agents, step_num=10)
    except Exception as e:
        pytest.fail(f"adjust_agent_demand_multiplier raised an exception: {e}")

def test_check_agent_bankruptcies_in_helpers():
    """
    Test that check_agent_bankruptcies returns agents that are bankrupt.
    """
    agents = [Agent(i) for i in range(3)]
    agents[0].ctx_balance = BANKRUPTCY_THRESHOLD - 10
    bankrupts = check_agent_bankruptcies(agents)
    assert agents[0] in bankrupts
    # Others should not be bankrupt if their balance is above threshold.
    assert all(agent.ctx_balance > BANKRUPTCY_THRESHOLD for agent in agents if agent not in bankrupts)

def test_tax_and_redistribute():
    """
    Test that tax_agents subtracts taxes from agent balances and redistribute_wealth adds equal shares.
    """
    # Create two agents with identical balances.
    agents = [Agent(i) for i in range(2)]
    for agent in agents:
        agent.ctx_balance = 100.0
    total_taxes = tax_agents(agents, TAX_RATE, [])
    # Each agent should have been taxed TAX_RATE * 100.
    for agent in agents:
        expected_balance = 100.0 - (100.0 * TAX_RATE)
        assert np.isclose(agent.ctx_balance, expected_balance)
    # Now redistribute the collected taxes.
    # Record balances before redistribution.
    balances_before = [agent.ctx_balance for agent in agents]
    redistribute_wealth(agents, total_taxes, [])
    redistribution = total_taxes / len(agents)
    for before, agent in zip(balances_before, agents):
        assert np.isclose(agent.ctx_balance, before + redistribution)

def test_adjust_resource_capacity():
    """
    Test that adjust_resource_capacity increases the capacity based on economic output.
    """
    resource = Resource(0)
    resource.capacity = 100.0
    total_economic_output = 500.0
    adjust_resource_capacity([resource], total_economic_output)
    expected_capacity = min(MAX_RESOURCE_CAPACITY, 100.0 * (1 + RESOURCE_CAPACITY_MULTIPLIER * total_economic_output))
    assert np.isclose(resource.capacity, expected_capacity)

def test_get_agent_balances():
    """
    Test that get_agent_balances returns a list of agent balances.
    """
    agents = [Agent(i) for i in range(4)]
    for i, agent in enumerate(agents):
        agent.ctx_balance = 50.0 + i * 10
    balances = get_agent_balances(agents)
    assert isinstance(balances, list)
    np.testing.assert_allclose(balances, [50.0, 60.0, 70.0, 80.0])

def test_get_resource_load_and_prices():
    """
    Test that get_resource_load_and_prices returns two lists corresponding to resource prices and loads.
    """
    resources = [Resource(i) for i in range(3)]
    for i, resource in enumerate(resources):
        resource.price = BASE_RESOURCE_COST + i
        resource.current_load = 10 * i
    prices, loads = get_resource_load_and_prices(resources)
    assert prices == [resource.price for resource in resources]
    assert loads == [resource.current_load for resource in resources]

def test_get_total_economic_output():
    """
    Test that get_total_economic_output correctly sums agent balances and resource values.
    """
    # Create two agents with known balances.
    agents = [Agent(i) for i in range(2)]
    agents[0].ctx_balance = 100.0
    agents[1].ctx_balance = 150.0
    # Create two resources with known prices and loads.
    resource1 = Resource(0)
    resource1.price = 2.0
    resource1.current_load = 30.0
    resource2 = Resource(1)
    resource2.price = 3.0
    resource2.current_load = 20.0
    resources = [resource1, resource2]
    expected_total = (100.0 + 150.0) + (2.0 * 30.0 + 3.0 * 20.0)
    total_output = get_total_economic_output(agents, resources)
    assert np.isclose(total_output, expected_total)

def test_calculate_gini_coefficient():
    """
    Test calculate_gini_coefficient with a simple distribution.
    """
    # For a perfectly equal distribution, Gini should be 0.
    equal_balances = [100, 100, 100, 100]
    gini_equal = calculate_gini_coefficient(equal_balances)
    assert np.isclose(gini_equal, 0.0)
    
    # For a simple unequal distribution, compute manually.
    balances = [0, 0, 100, 100]
    # The expected value can be computed manually; here we test that it's > 0.
    gini_unequal = calculate_gini_coefficient(balances)
    assert gini_unequal > 0.0

# -----------------------------
# Main: Run tests if executed directly.
# -----------------------------
if __name__ == "__main__":
    pytest.main()
