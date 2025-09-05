# Governance and DAO Simulation

## Overview

This simulation subsystem implements a token-based governance mechanism, modeling the "who decides" layer of decentralized systems. It simulates DAOs where token holders vote on proposals that can modify parameters of other economic systems or allocate community treasury funds. The simulation compares different voting mechanisms (simple, quadratic, delegation) and their impacts on participation, wealth distribution, and governance outcomes.

## Key Features

* **Multiple Voting Mechanisms:** Supports simple voting, quadratic voting, and delegation-based governance.
* **Proposal System:** Agents can submit proposals to change parameters (e.g., tax rates from MCP simulation) or allocate treasury funds.
* **Treasury Management:** Simulates a community treasury that collects fees and allocates funds based on successful proposals.
* **Agent Behavior:** Models voter participation rates, proprietary behavior, and whale influence on outcomes.
* **Cross-System Integration:** Imports token holdings data from other simulations (e.g., Affiliate system) to initialize voter power.
* **Metrics Tracking:** Monitors voter turnout, Gini coefficient evolution, proposal success rates, and treasury sustainability.

## What the Code Does

The `main.py` script simulates a governance process over multiple time steps:

1. **Initialization:**
   - Creates voters with token holdings, possibly loaded from external simulation outputs.
   - Sets up treasury with initial funds.
   - Configures voting mechanism (simple, quadratic, or delegation).

2. **Simulation Loop:**
   - At each step, agents may submit proposals.
   - Participating voters cast votes on active proposals.
   - Proposals are resolved based on voting thresholds.
   - Successful proposals trigger treasury allocations or parameter changes.
   - Metrics are recorded (participation, Gini coefficient, etc.).

3. **Visualization and Analysis:**
   - Generates plots comparing metrics across different voting mechanisms.
   - Outputs summary statistics and trends.

## Mathematical Basis (`math.md`)

The `math.md` file provides a mathematical formulation of the governance simulation, including:

* **Notation Table:** Defines variables for voters, proposals, voting power, and treasury.
* **Problem Statement:** Formulates the governance dynamics.
* **Equations:** Mathematical expressions for voting power, proposal passage, treasury allocation, and Gini coefficient.
* **Solution Approach:** Discrete simulation methodology.
* **Analysis:** Explanation of key metrics and their interpretation.

## How to Use the Code

1. **Prerequisites:**
   - Python 3.x with numpy, matplotlib, pandas installed.

2. **Run the Simulation:**
   ```bash
   cd governance-dao/notebook
   python main.py
   ```

   The script will simulate governance under different voting mechanisms and generate comparison plots.

3. **Customize Parameters:**
   - Edit constants at the top of `main.py` to change number of voters, simulation steps, etc.
   - Modify voting mechanism in the main loop for specific analyses.

4. **Integration with Other Systems:**
   - The simulation attempts to load token holdings from `../affiliate/output.txt`.
   - Ensure other simulations have run and generated output files for cross-system integration.

## Repository Contents

* `main.py`: The core Python script implementing the governance simulation.
* `math.md`: Mathematical formulation and documentation.
* `output.png`: (Generated) Comparison plots for different voting mechanisms.
* `requirements.txt`: (Optional) Dependencies.

## Configuration Options

| Parameter                  | Description                                      |
|----------------------------|--------------------------------------------------|
| `NUM_VOTERS`              | Total number of voting agents                    |
| `SIMULATION_STEPS`         | Duration of the simulation in timesteps         |
| `TREASURY_INITIAL`         | Starting treasury funds                         |
| `PROPOSAL_SUBMISSION_RATE` | Probability of new proposal per timestep        |
| `MIN_VOTING_THRESHOLD`     | Minimum vote ratio for proposal passage         |
| `VOTER_PARTICIPATION_RATE` | Base participation probability                   |
| `WHALE_THRESHOLD_MULTIPLIER` | Threshold for classifying "whale" voters     |

## Integration with Other Systems

The simulation integrates with existing subsystems by:

- **Importing Data:** Loads token holdings from Affiliate simulation to set initial voter power.
- **Proposal Targets:** Proposals can reference components of other systems (e.g., "adjust MCP tax rate").
- **Parameter Coupling:** Proposal execution can modify global parameters that affect other simulations.

## Potential Extensions

This governance simulation provides a foundation for exploring advanced DAO mechanics:

* **Advanced Voting:** Implement approval voting, ranked-choice voting, or time-locked governance.
* **Attack Modeling:** Simulate hacking attempts, bribery, or populist manipulation.
* **Multi-DAO Networks:** Model interconnected DAOs with cross-governance.
* **Dynamic Participation:** Add incentives for voter turnout or delegate reputation systems.
* **Real-World Data:** Import actual DAO voting data for validation.

## Output Interpretation

The simulation generates insights into:

- **Participation Rates:** How different mechanisms affect voter engagement.
- **Inequality Trends:** Evolution of wealth distribution through governance decisions.
- **Proposal Success:** Effectiveness of the voting system in implementing changes.
- **Treasury Health:** Sustainability of community fund allocations.

This simulation bridges the financial mechanics of token economies with the governance that controls them, providing a comprehensive view of decentralized decision-making processes.