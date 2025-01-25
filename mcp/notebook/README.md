# mcp

This repository contains a Python script (`main.py`) that simulates a simple agent-based economy with resources. The simulation models the interactions between agents who demand and consume resources, and resources that have limited capacity and regenerate over time. The goal is to explore the dynamics of such a system, including wealth distribution, resource prices, and the impact of various economic parameters.

A detailed mathematical formulation of this simulation is available in the accompanying paper, [`math.md`](math.md).

## Overview

The simulation features:

*   **Agents:** Individual entities with a context balance (representing wealth), preferences for different resources, and the ability to request and consume resources. Agents earn income, incur expenses, and pay taxes. They can also go bankrupt if their balance falls below a certain threshold.
*   **Resources:** Limited commodities with a capacity, current load, and price. Resource prices fluctuate based on demand. Resources can regenerate and their capacity can adjust based on the overall economic output.
*   **Market Mechanism:** Agents request resources based on their preferences and affordability. Resources are allocated based on availability.
*   **Economic Dynamics:** The simulation models key economic processes like price formation, resource allocation, wealth accumulation, and redistribution through taxation.

## Key Features

*   **Dynamic Resource Pricing:** Resource prices adjust based on the ratio of current load to capacity.
*   **Resource Regeneration and Capacity Adjustment:** Resources replenish over time, and their maximum capacity can adapt based on the overall economic activity.
*   **Agent Behavior:** Agents have varying resource preferences, adjust their demand, earn income, incur expenses, and can become bankrupt.
*   **Taxation and Redistribution:** The simulation includes a taxation mechanism where a portion of agents' balances is collected and redistributed among the non-bankrupt agents.
*   **Parameter Experimentation:** The script includes functionality to systematically vary key economic parameters and visualize their impact on simulation outcomes.

## Mathematical Foundation

The underlying logic of the simulation is described in detail in the accompanying mathematical paper, [`math.md`](math.md). This paper provides a formal mathematical representation of the agents, resources, and their interactions, including the equations governing their behavior. Refer to this document for a rigorous understanding of the model.

## How It Works

The simulation proceeds in discrete time steps. At each step:

1. **Resource Prices are Updated:** Based on the current demand and capacity.
2. **Agents Request Resources:**  Considering their preferences, resource prices, and their own balance.
3. **Resources are Allocated:** Based on availability and agent requests.
4. **Resource Load is Updated.**
5. **Resource Deallocation Occurs:** A portion of the loaded resources is removed.
6. **Resources Regenerate:** Their capacity increases based on a regeneration rate.
7. **Resource Capacity Adjusts:** Based on the total economic output.
8. **Agents Adjust Their Needs:** Their resource preferences change randomly.
9. **Agents Adjust Their Demand Multiplier:** Increasing their overall demand over time.
10. **Agents Receive Income:**  A base income with a potential dynamic component.
11. **Agents Incur Expenses.**
12. **Agents Pay Taxes.**
13. **Wealth is Redistributed:**  Tax revenue is distributed among non-bankrupt agents.
14. **Agent Bankruptcies are Checked:** Agents with balances below a threshold are marked as bankrupt and removed from the simulation.

## Parameters

The simulation is governed by several key parameters that can be adjusted to explore different economic scenarios. These include:

*   `NUM_AGENTS`: The number of agents in the simulation.
*   `NUM_RESOURCES`: The number of different resources.
*   `SIMULATION_STEPS`: The duration of the simulation.
*   `INITIAL_CTX_BALANCE`: The starting wealth of each agent.
*   `RESOURCE_CAPACITY`: The initial capacity of each resource.
*   `BASE_RESOURCE_COST`: The base price of resources.
*   `PRICE_ELASTICITY`:  How sensitive resource prices are to changes in demand.
*   `DEALLOCATION_RATE`: The rate at which loaded resources are removed.
*   `AGENT_INCOME`: The base income for each agent.
*   `RESOURCE_REGEN_RATE`: The rate at which resources regenerate.
*   `MAX_RESOURCE_CAPACITY`: The maximum capacity a resource can reach.
*   `AGENT_EXPENSE_RATE`: The rate at which agents incur expenses.
*   `MIN_AGENT_BALANCE`: The minimum balance an agent can have before being unable to make requests.
*   `BANKRUPTCY_THRESHOLD`: The balance below which an agent is considered bankrupt.
*   `DYNAMIC_INCOME_MULTIPLIER`:  Influences how average resource prices affect agent income.
*   `DYNAMIC_REGEN_MULTIPLIER`: Influences how average agent balance affects resource regeneration.
*   `AGENT_INCOME_CEILING`: The maximum income an agent can receive.
*   `TAX_RATE`: The percentage of an agent's balance that is taxed.
*   `RESOURCE_CAPACITY_MULTIPLIER`: Influences how total economic output affects resource capacity.
*   `INITIAL_IMBALANCE`: A boolean flag to introduce initial wealth disparity among agents.
*   `IMBALANCE_STRENGTH`:  The degree of initial wealth imbalance.

## Experimentation

The script includes a section for parameter experimentation. It systematically varies the following parameters and runs the simulation for each value:

*   `price_elasticity`
*   `resource_regen_rate`
*   `tax_rate`
*   `agent_expense_rate`

The results of these experiments are visualized in a plot (`parameter_impact.png`) showing the impact of each parameter on the average final agent balance, Gini coefficient (a measure of wealth inequality), number of bankruptcies, and average final resource price.

## Running the Code

To run the simulation, you need Python 3 and the following libraries:

*   `numpy`
*   `matplotlib`

You can install the dependencies using pip:

```bash
pip install numpy matplotlib
```

To execute the simulation, simply run the Python script:

```bash
python main.py
```

The script will perform the parameter experimentation and save the resulting plots to `parameter_impact.png`. It will also output some analysis to the console.

## Repository Contents

*   `main.py`: The main Python script containing the simulation code.
*   `math.md`: The mathematical formulation of the simulation model.
*   `parameter_impact.png`:  The generated plot showing the impact of parameter variations.

## License

MIT-0 License