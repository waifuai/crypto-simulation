# Token Economy Simulation Suite

License: MIT-0

## Project Goal

This repository provides a suite of simulation systems designed to model, analyze, and understand the complex dynamics of various token economy mechanisms. Using Agent-Based Modeling (ABM) and discrete event simulation, these tools allow researchers, designers, and analysts to explore the behavior of crypto-economic systems under different conditions and parameter settings, aiming to inform protocol design and economic policy.

## Core Concepts

*   **Agent-Based Modeling (ABM):** A computational modeling paradigm that simulates the actions and interactions of autonomous agents (both individual and collective entities such as organizations or groups) within an environment. ABM allows observing emergent system-level behavior from micro-level agent rules.
*   **Token Economy Simulation:** Applying ABM and other simulation techniques to model systems involving digital tokens. This includes analyzing token issuance, distribution, utility, governance, and the behavior of participants (agents) interacting within the defined economic rules and incentives.

## Overview of Simulation Systems

This suite contains five distinct simulation systems:

1.  **Affiliate Network Simulation (`affiliate/`)**
2.  **Airdrop Strategy Engine (`airdrop/`)**
3.  **Bonding Curve Laboratory (`bonding-curve/`)**
4.  **Model Context Protocol Simulation (`mcp/`)**
5.  **Governance and DAO Simulation (`governance-dao/`)**

Each system addresses different facets of crypto-economic design and analysis.

## General Assumptions & Limitations

*   **Rationality (Bounded):** Agents are generally assumed to act in their self-interest based on the information available to them, but may not be perfectly rational or omniscient. Specific agent logic varies per model.
*   **Environment:** Simulations occur within a defined computational environment; external market factors or unforeseen real-world events are typically not modeled unless explicitly included.
*   **Simplification:** Models are necessarily simplifications of reality, focusing on specific mechanisms. They may omit certain complexities for tractability.
*   **Scope:** Each model focuses on its defined scope (e.g., bonding curves, airdrops). Interactions *between* these mechanisms are generally explored via separate cross-system analysis rather than a single unified simulation.

## Validation & Verification Approach

Each simulation model undergoes:

*   **Verification:** Code testing (unit tests, integration tests) to ensure the simulation logic correctly implements the intended model design. Code reviews and debugging are standard practice.
*   **Validation:** Comparing simulation outputs against theoretical expectations, known patterns, or (where applicable) real-world data analogues. Sensitivity analysis is used to understand the impact of parameter changes. (Note: Detailed validation reports may reside within individual subsystem documentation).

## Data

The simulations primarily use synthetically generated agent populations and parameters based on defined distributions and archetypes. Specific configurations may allow for initialization with external datasets where appropriate (refer to individual subsystem documentation).

---

## 1. Affiliate Network Simulation (`affiliate/`)

*   **[Detailed Documentation](affiliate/README.md)**
*   **Core Mechanism:** Dynamic bonding curves with referral incentives. Models how affiliate programs influence token price and distribution on multiple parallel bonding curves.
*   **Key Agents:** Affiliates (promoting tokens), Buyers (acquiring tokens), Whale Agents (large holders with market impact).
*   **Outputs:** Time-series data on token prices, supply, commission rates, agent balances, transaction logs (`affiliate/output.txt`).

### Key Features:
- Multi-token system with 5 simultaneous bonding curves
- Whale agent detection and behavior modeling
- Adaptive commission rates (0-20% range)
- Moving average price stabilization
- Transaction fee/burn rate mechanisms

```python
# Custom bonding curve configuration example
from affiliate.bonding_curves import exponential_bonding_curve
token = Token("VIP", 10000, 1.0,
    lambda s: exponential_bonding_curve(s, a=1.2, k=0.0007))
```

### Execution:
```bash
cd affiliate
python main.py --num_simulation_steps 500 --num_affiliates 10
```

---

## 2. Airdrop Strategy Engine (`airdrop/`)

*   **[Detailed Documentation](airdrop/README.md)**
*   **Core Mechanism:** Multi-parameter airdrop optimization. Simulates the impact of different airdrop design choices on token price stability, holder retention, and network growth.
*   **Key Agents:** Airdrop Recipients (with varying holding/selling behaviors), General Market Participants.
*   **Outputs:** Simulation results comparing price stability, holder retention metrics, and token velocity across different strategies (`airdrop/output.txt`).

### Strategy Matrix:
| Parameter        | Options                              | Optimization Goal          |
|-------------------|--------------------------------------|----------------------------|
| Vesting Type      | Dynamic Price, Activity, Linear      | Price Stability            |
| Distribution      | Uniform, Tiered, Lottery             | Long-term Holder Retention |
| Criteria          | Holdings, Activity, Random           | Network Growth             |
| Vesting Periods   | 1-24 months                          | Token Velocity Reduction   |


### Execution:
```bash
cd airdrop
python main.py --strategy_type tiered --vesting dynamic_price
```

---

## 3. Bonding Curve Laboratory (`bonding-curve/`)

*   **[Detailed Documentation](bonding-curve/README.md)**
*   **Core Mechanism:** Evolutionary parameter optimization for various bonding curve types. Aims to find optimal curve parameters based on defined objectives (e.g., price stability, capital efficiency).
*   **Key Agents:** Buyers, Sellers interacting with the bonding curve contract.
*   **Outputs:** Optimized parameter sets, performance metrics for different curve types, simulation trajectories (`bonding-curve/output.txt`).

### Curve Types:
1.  **Linear:** `price = m*supply + b`
2.  **Exponential:** `price = a*e^(k*supply)`
3.  **Sigmoid:** `price = K/(1 + e^(-k(supply-S0)))`
4.  **Multi-segment:** Hybrid linear-exponential

```python
# Parameter optimization example
optimal_params = optimize_bonding_curve('sigmoid',
    param_ranges={
        'k': (0.01, 0.05),
        's0': (800, 1200),
        'k_max': (5, 15)
    })
```

### Execution:
```bash
cd bonding-curve
python main.py --curve_type sigmoid --optimize_params
```

---

## 4. Model Context Protocol Simulation (`mcp/`)

*   **[Detailed Documentation](mcp/README.md)**
*   **Core Mechanism:** Simulation of interactions within the Model Context Protocol (MCP) ecosystem. MCP is an open standard enabling AI applications (Clients) to connect with external tools and data sources (Servers).
*   **Key Agents:** MCP Clients (e.g., simulated AI applications), MCP Servers (exposing tools/resources).
*   **Outputs:** Data on request latency, server load, tool usage frequency, resource contention, success/failure rates (`mcp/output.txt`). *(Outputs depend on specific metrics implemented)*.

### Key Simulated Aspects:
- Client request generation patterns.
- Server handling of concurrent requests, queuing.
- Tool discovery and simulated execution time/cost.
- Resource access simulation (latency, availability).
- Network latency effects.

### Execution: *(Needs Verification)*
*(Verify arguments based on `mcp/main.py`)*
```bash
cd mcp
# Example: python main.py --num_clients 50 --num_servers 5
python main.py # <-- Add relevant arguments for MCP simulation
```

---

## 5. Governance and DAO Simulation (`governance-dao/`)

*   **[Detailed Documentation](governance-dao/README.md)**
*   **Core Mechanism:** Token-based governance simulation modeling DAO decision-making. Simulates voters submitting proposals, casting votes, and treasury allocations across different voting mechanisms (simple, quadratic, delegation).
*   **Key Agents:** Voters (holders casting votes), Proposal Submitters, Treasury Managers.
*   **Outputs:** Voter turnout rates, proposal success metrics, Gini coefficient evolution, treasury trends across voting mechanisms (`governance-dao/output.txt`).

### Key Features:
- Multiple voting mechanisms: Simple (1 vote per token), Quadratic (diminishing returns), Delegation (representatives)
- Treasury management with fund allocation
- Whale voter influence modeling
- Cross-system integration with other simulations
- Participation rate and inequality tracking

### Execution:
```bash
cd governance-dao/notebook
python main.py
```

---

## Unified Installation

Follow these steps to set up the environment and install dependencies for all simulation systems.

```bash
# Create virtual environment (recommended)
python -m venv econ-sim
source econ-sim/bin/activate  # On Windows use `econ-sim\Scripts\activate`

# Install core dependencies (using --user if not in a venv)
pip install --user numpy>=1.21 pandas>=1.3 scipy>=1.7 matplotlib>=3.4

# Install subsystem-specific requirements (using --user if not in a venv)
pip install --user -r affiliate/requirements.txt
pip install --user -r airdrop/requirements.txt
pip install --user -r bonding-curve/requirements.txt
pip install --user -r mcp/requirements.txt
```
*Note: If using a virtual environment, the `--user` flag is typically not needed.*

---

## Cross-System Analysis

The outputs from individual simulations can be combined for comparative analysis. The example below demonstrates plotting key metrics from each system side-by-side. (Ensure `matplotlib` is installed).

```python
import matplotlib.pyplot as plt
# Assume data loading functions exist, e.g., load_affiliate_data()
# affiliate_data = load_affiliate_data('affiliate/output.txt')
# airdrop_data = load_airdrop_data('airdrop/output.txt')
# bonding_data = load_bonding_data('bonding-curve/output.txt')
# mcp_data = load_mcp_data('mcp/output.txt') # <-- Update loader if needed for MCP data

# Example analysis function (conceptual)
def analyze_results(affiliate_data, airdrop_data, bonding_data, mcp_data):
    """
    Compares key outputs from the different simulation systems.
    (Requires actual data loading and potentially more specific plotting logic)
    """
    fig, axs = plt.subplots(2, 2, figsize=(15,10))
    fig.suptitle('Cross-System Simulation Analysis Overview')

    # Plot affiliate commission rates (Example metric)
    # axs[0,0].plot(affiliate_data['time'], affiliate_data['average_commission_rate'])
    axs[0,0].set_title('Affiliate Commission Dynamics')
    axs[0,0].set_xlabel('Time Steps')
    axs[0,0].set_ylabel('Avg. Commission Rate')

    # Plot airdrop price trajectories (Example metric)
    # for strategy_name, strategy_data in airdrop_data.items():
    #     axs[0,1].plot(strategy_data['time'], strategy_data['price_history'], label=strategy_name)
    axs[0,1].set_title('Airdrop Price Performance Comparison')
    axs[0,1].set_xlabel('Time Steps')
    axs[0,1].set_ylabel('Token Price')
    axs[0,1].legend()

    # Plot bonding curve parameter space (Conceptual - requires specific plotting function)
    # plot_3d_surface(bonding_data, ax=axs[1,0]) # Replace with actual plotting
    axs[1,0].set_title('Bonding Curve Optimization Landscape')


    # Plot MCP metrics (Example: Average Request Latency)
    # axs[1,1].plot(mcp_data['time'], mcp_data['avg_request_latency']) # <-- Update metric based on actual output
    axs[1,1].set_title('MCP Interaction Dynamics') # <-- Updated title
    axs[1,1].set_xlabel('Time Steps')
    axs[1,1].set_ylabel('Avg. Request Latency (ms)') # <-- Example updated label

    plt.tight_layout(rect=[0, 0.03, 1, 0.95]) # Adjust layout to prevent title overlap
    plt.show()

# Example usage (requires data loading)
# analyze_results(affiliate_data, airdrop_data, bonding_data, mcp_data)
```
*Note: The analysis script requires implementing data loading and potentially more specific plotting logic based on the actual contents of `output.txt` files, especially for the MCP simulation.*

---

## License

This project is licensed under the MIT-0 License. See the [LICENSE](LICENSE) file for details.

## How to Cite

If you use this simulation suite in your research or work, please cite it appropriately. (A suggested citation format will be added here once the project reaches a stable version or publication).